"""
Report Agent - Generates professional PDF reports
Responsible for:
- Creating HTML report template
- Generating PDF from HTML
"""

import logging
from jinja2 import Template
from pathlib import Path
from app.agents.state import WorkflowState

logger = logging.getLogger(__name__)


class ReportAgent:
    """Generates professional consulting-style reports"""
    
    def __init__(self):
        self.template_dir = Path("app/templates")
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Generate report
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with report HTML
        """
        logger.info(f"Report Agent started for: {state.company_name}")
        
        try:
            # Generate HTML report
            html_content = self._generate_html_report(state)
            state.report_html = html_content

            state.add_step("report_generated")
            logger.info("Report Agent completed successfully")

        except Exception as e:
            logger.error(f"Report Agent error: {str(e)}", exc_info=True)
            state.add_error("report", str(e))
            # Don't leave report_html empty — downstream PDF step still needs
            # something to render (and ReportLab fallback can use state directly).
            state.report_html = state.report_html or f"<html><body><h1>{state.company_name}</h1></body></html>"

        return state
    
    def _generate_html_report(self, state: WorkflowState) -> str:
        """Generate professional HTML report"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Intelligence Report - {state.company_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            line-height: 1.6;
        }}
        .page {{
            page-break-after: always;
            padding: 40px;
            min-height: 1000px;
            background: white;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #0066cc;
        }}
        .logo {{
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 20px;
        }}
        h1 {{
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }}
        h2 {{
            font-size: 24px;
            color: #0066cc;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #0066cc;
            padding-left: 15px;
        }}
        h3 {{
            font-size: 18px;
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .card {{
            background: #f8f9fa;
            border-left: 4px solid #0066cc;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 4px;
        }}
        .score-container {{
            display: flex;
            gap: 30px;
            margin: 20px 0;
        }}
        .score-box {{
            flex: 1;
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .score-value {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .score-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        li {{
            margin-bottom: 10px;
        }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .comparison-table th {{
            background: #0066cc;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        .comparison-table td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        .comparison-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        .recommendation {{
            background: #e8f4f8;
            border-left: 4px solid #0099cc;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }}
        .finding {{
            background: #fff8e1;
            border-left: 4px solid #ffc107;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        .finding.good {{
            background: #e8f5e9;
            border-left-color: #4caf50;
        }}
        .finding.critical {{
            background: #ffebee;
            border-left-color: #f44336;
        }}
        .data-source {{
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>

<!-- PAGE 1: COVER & EXECUTIVE SUMMARY -->
<div class="page">
    <div class="header">
        <div class="logo">📊 SimplifIQ AI Prospect Intelligence</div>
        <h1>{state.company_name}</h1>
        <p style="color: #666; font-size: 16px;">Company Intelligence Report</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <div class="card">
            <p>{state.company_description or 'Company profile being analyzed.'}</p>
        </div>
    </div>
    
    <div class="section">
        <h2>Key Metrics</h2>
        <div class="score-container">
            <div class="score-box">
                <div class="score-value">{state.website_score:.0f}</div>
                <div class="score-label">Website Health Score</div>
            </div>
            <div class="score-box" style="background: linear-gradient(135deg, #00a86b 0%, #008c4a 100%);">
                <div class="score-value">{state.confidence_score:.0f}%</div>
                <div class="score-label">Analysis Confidence</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>Company Details</h2>
        <p><strong>Industry:</strong> {state.industry or 'Not specified'}</p>
        <p><strong>Website:</strong> {state.website_url}</p>
        <p><strong>Technologies:</strong> {', '.join(state.tech_stack) if state.tech_stack else 'Not identified'}</p>
    </div>
</div>

<!-- PAGE 2: ANALYSIS & FINDINGS -->
<div class="page">
    <div class="header">
        <h1>Business Analysis</h1>
    </div>
    
    <div class="section">
        <h2>Strengths</h2>
        <ul>
            {''.join(f'<li>{strength}</li>' for strength in state.strengths[:4])}
        </ul>
    </div>
    
    <div class="section">
        <h2>Growth Opportunities</h2>
        <ul>
            {''.join(f'<li>{opp}</li>' for opp in state.opportunities[:4])}
        </ul>
    </div>
    
    <div class="section">
        <h2>Pain Points Identified</h2>
        <ul>
            {''.join(f'<li>{pain}</li>' for pain in state.pain_points[:4])}
        </ul>
    </div>
    
    <div class="section">
        <h2>Website Audit Findings</h2>
        {''.join(f'''
        <div class="finding {'good' if finding.get('status') == 'good' else 'critical' if finding.get('severity') == 'high' else ''}">
            <strong>{finding.get('issue')}:</strong> {finding.get('recommendation', '')}
        </div>
        ''' for finding in state.website_findings[:5])}
    </div>
</div>

<!-- PAGE 3: COMPETITIVE ANALYSIS -->
<div class="page">
    <div class="header">
        <h1>Competitive Intelligence</h1>
    </div>
    
    <div class="section">
        <h2>Identified Competitors</h2>
        <p>Our analysis identified the following key competitors:</p>
        <ul>
            {''.join(f'<li><strong>{comp}</strong> - {state.competitor_data.get(comp, {}).get("positioning", "Competitive player in the market")}</li>' for comp in state.competitors[:3])}
        </ul>
    </div>
    
    <div class="section">
        <h2>Recent News & Updates</h2>
        {''.join(f'''
        <div class="card">
            <h3>{news.get('title', 'News Article')}</h3>
            <p>{news.get('snippet', '')[:200]}...</p>
        </div>
        ''' for news in state.recent_news[:3])}
    </div>
    
    <div class="footer">
        <p>Data Sources: {', '.join(state.data_sources)}</p>
    </div>
</div>

<!-- PAGE 4: RECOMMENDATIONS & NEXT STEPS -->
<div class="page">
    <div class="header">
        <h1>Strategic Recommendations</h1>
    </div>
    
    <div class="section">
        <h2>Actionable Recommendations</h2>
        {''.join(f'''
        <div class="recommendation">
            <h3>Action {i+1}</h3>
            <p>{rec}</p>
        </div>
        ''' for i, rec in enumerate(state.recommendations[:5]))}
    </div>
    
    <div class="section">
        <h2>Next Steps</h2>
        <div class="card">
            <p>Based on this comprehensive analysis, we recommend scheduling a consultation to discuss:</p>
            <ul>
                <li>Specific growth opportunities for your business</li>
                <li>Competitive positioning strategies</li>
                <li>Digital transformation initiatives</li>
                <li>Personalized implementation roadmap</li>
            </ul>
        </div>
    </div>
    
    <div class="section">
        <p style="text-align: center; margin-top: 60px; color: #666;">
            This report was generated by SimplifIQ AI Prospect Intelligence Engine<br>
            {state.lead_name} • {state.lead_email}
        </p>
    </div>
</div>

</body>
</html>
"""
        return html
