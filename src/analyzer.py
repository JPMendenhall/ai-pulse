import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_ai_news(news_items):
    """
    Send news articles to GPT-4o-mini for analysis
    Returns structured daily report
    """
    
    if not news_items:
        print("❌ No news to analyze")
        return None
    
    # Format news for the LLM
    news_text = "\n\n".join([
        f"**{item['title']}**\n"
        f"Source: {item['source']}\n"
        f"Description: {item['description']}\n"
        f"URL: {item['url']}"
        for item in news_items
    ])
    
    context = f"""
Analyze today's AI and technology news. You're enthusiastic about innovation but also realistic about challenges and limitations.

TODAY'S AI NEWS:
{news_text}

IMPORTANT: This is a ROUNDUP newsletter. Cover MULTIPLE distinct stories across sections. Don't let one story dominate the entire report.

Format your response with these sections:

**HEADLINE OF THE DAY**
One punchy sentence capturing the most significant TECHNICAL development in AI today. Prioritize: new models > new products > research breakthroughs.

**WHAT'S NEW**
Cover 3-4 DIFFERENT announcements from today. Each gets 1-2 sentences. Examples:
- DeepMind's AlphaGenome for DNA analysis
- Moltbot's new capabilities
- Microsoft Copilot updates
- Any other model releases or product launches
Don't spend all 3-4 sentences on ONE thing - spread it across multiple stories.

**BUSINESS MOVES**
Cover 2-3 DIFFERENT business developments. Examples:
- Funding rounds (who raised how much)
- Partnerships or acquisitions
- Company restructuring or leadership changes
If multiple things happened, mention them all briefly. If quiet, say "Quiet on the business front."

**WHY IT MATTERS**
Explain the practical implications of 2-3 of the most important announcements above. How do they affect developers, businesses, or users? What changes in practice? Mix enthusiasm with realism.

**THE BOTTOM LINE**
Synthesize the day's news into one key insight. What's the big-picture takeaway from today's multiple developments? 2-3 sentences.

Voice guidelines:
- Cover breadth, not depth - this is a news roundup
- Multiple stories > one deep story
- Enthusiastic about genuine innovation
- Realistic about challenges and limitations
- Accessible language, avoid excessive jargon
"""

    print("🤖 Sending news to AI for analysis...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You're an AI technology analyst creating a daily NEWS ROUNDUP. Your job is to cover MULTIPLE stories, not deep-dive one topic. Mention 3-4 different developments in What's New. Cover 2-3 business items. You prioritize breadth over depth - think newsletter summary, not long-form article. Technical AI developments come first, but you cover the full landscape of what happened today."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        analysis = response.choices[0].message.content
        
        print("✅ AI analysis complete!\n")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Test with mock data
    print("Testing AI Analyzer with mock data\n")
    print("="*70)
    
    mock_news = [
        {
            'title': 'OpenAI releases GPT-5 with reasoning capabilities',
            'description': 'New model shows significant improvements in multi-step reasoning',
            'source': 'TechCrunch',
            'url': 'https://example.com'
        },
        {
            'title': 'Google DeepMind announces AlphaFold 3',
            'description': 'Breakthrough in protein structure prediction',
            'source': 'Nature',
            'url': 'https://example.com'
        }
    ]
    
    analysis = analyze_ai_news(mock_news)
    
    if analysis:
        print("="*70)
        print("AI ANALYSIS:")
        print("="*70)
        print(analysis)