import os
import sys
from datetime import datetime

# Add src to path so imports work
sys.path.append(os.path.dirname(__file__))

from collectors.ai_news import get_ai_news
from analyzer import analyze_ai_news
from reporter import generate_daily_html_report

def generate_daily_report():
    """
    Main function - orchestrates daily AI Pulse report
    """
    
    print(f"\n⚡ AI PULSE - Daily Report")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    print("="*70)
    
    # Step 1: Collect news
    print("\n📰 Collecting AI news...")
    news = get_ai_news()
    
    if not news:
        print("❌ Failed to collect news - aborting")
        return None
    
    print(f"✅ Collected {len(news)} articles")
    
    # Step 2: Analyze with AI
    print("\n🤖 Analyzing with AI...")
    analysis = analyze_ai_news(news)
    
    if not analysis:
        print("❌ Failed to analyze news - aborting")
        return None
    
    print("✅ Analysis complete")
    
    # Step 3: Generate HTML report
    print("\n📄 Generating HTML report...")
    filepath = generate_daily_html_report(news, analysis)
    
    print("\n" + "="*70)
    print("✅ DAILY REPORT COMPLETE!")
    print(f"📂 Saved to: {filepath}")
    print("="*70 + "\n")
    
    return filepath

if __name__ == "__main__":
    try:
        generate_daily_report()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)