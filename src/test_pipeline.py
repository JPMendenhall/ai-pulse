import sys
sys.path.append('src')

from collectors.ai_news import get_ai_news
from analyzer import analyze_ai_news
from reporter import generate_daily_html_report

def test_full_pipeline():
    """Test the complete news collection, analysis, and HTML generation pipeline"""
    
    print("🚀 AI PULSE - Testing Full Pipeline")
    print("="*70)
    print()
    
    # Step 1: Collect news
    print("STEP 1: COLLECTING NEWS")
    print("-"*70)
    news = get_ai_news()
    
    if not news:
        print("❌ Failed to collect news")
        return
    
    print(f"\n✅ Collected {len(news)} articles\n")
    
    # Step 2: Analyze with AI
    print("STEP 2: ANALYZING WITH AI")
    print("-"*70)
    analysis = analyze_ai_news(news)
    
    if not analysis:
        print("❌ Failed to analyze news")
        return
    
    print("\n✅ Analysis complete\n")
    
    # Step 3: Generate HTML report
    print("STEP 3: GENERATING HTML REPORT")
    print("-"*70)
    filepath = generate_daily_html_report(news, analysis)
    
    # Step 4: Display results
    print("\n" + "="*70)
    print("TODAY'S AI PULSE REPORT")
    print("="*70)
    print()
    print(analysis)
    print()
    print("="*70)
    print(f"✅ Pipeline complete! Open: {filepath}")

if __name__ == "__main__":
    test_full_pipeline()