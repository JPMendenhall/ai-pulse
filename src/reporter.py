import os
from datetime import datetime
from jinja2 import Template
import markdown
import re

def format_analysis_for_html(analysis_text):
    """Convert markdown-style analysis to HTML with proper section headers"""
    # Convert **SECTION TITLE** to <h2>SECTION TITLE</h2>
    # This regex finds lines that are just bold text (section headers)
    analysis_text = re.sub(
        r'\*\*(.*?)\*\*\s*$',
        r'<h2>\1</h2>',
        analysis_text,
        flags=re.MULTILINE
    )
    
    # Convert remaining markdown to HTML
    html = markdown.markdown(analysis_text)
    return html

def generate_daily_html_report(news_items, analysis):
    """Generate daily HTML report"""
    
    # Read template
    template_path = os.path.join('templates', 'daily_report.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Format timestamp
    timestamp = datetime.now()
    date_str = timestamp.strftime('%B %d, %Y')
    time_str = timestamp.strftime('%I:%M %p ET')
    day_of_week = timestamp.strftime('%A')
    
    # Convert analysis to HTML
    analysis_html = format_analysis_for_html(analysis)
    
    # Render template
    html = template.render(
        date=date_str,
        time=time_str,
        day=day_of_week,
        news_items=news_items,
        analysis_html=analysis_html
    )
    
    # Save to reports/daily/ with date format
    filename = timestamp.strftime('report_%Y%m%d.html')
    filepath = os.path.join('reports', 'daily', filename)
    
    # Ensure directory exists
    os.makedirs(os.path.join('reports', 'daily'), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Daily report saved to: {filepath}")
    
    return filepath

if __name__ == "__main__":
    print("Reporter module - use from main pipeline")