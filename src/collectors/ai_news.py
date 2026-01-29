import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_ai_news():
    """
    Fetch AI and technology news from NewsAPI
    Returns structured news data
    """
    
    api_key = os.getenv('NEWSAPI_KEY')
    
    if not api_key:
        print("❌ NEWSAPI_KEY not found in .env")
        return None
    
    # Get news from last 7 days (NewsAPI free tier limitation)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
        
    # Simpler query - just AI keywords, filter crypto out
    query = (
        '("artificial intelligence" OR "machine learning" OR '
        '"OpenAI" OR "Anthropic" OR "ChatGPT" OR "Claude" OR '
        '"Google Gemini" OR "Microsoft Copilot" OR "GitHub Copilot" OR '
        '"Meta AI" OR "AI model" OR "LLM" OR "large language model" OR '
        '"generative AI" OR "GPT-4" OR "GPT-5" OR "AI assistant" OR '
        '"neural network" OR "Moltbot") '
        '-crypto -cryptocurrency -bitcoin -blockchain -"Ai Weiwei" -stock -stocks'
    )
    
    url = 'https://newsapi.org/v2/everything'
    


    params = {
        'q': query,
        'from': yesterday,
        'to': today,
        'sortBy': 'publishedAt',  # Most recent first
        'language': 'en',
        'pageSize': 50,
        'apiKey': api_key
    }
    
    try:
        print("📰 Fetching AI news from NewsAPI...")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] != 'ok':
            print(f"❌ NewsAPI error: {data.get('message', 'Unknown error')}")
            return None
        
        articles = data.get('articles', [])
        
        if not articles:
            print("⚠️  No articles found")
            return []
        
        # Filter out low-quality sources manually
        excluded_sources = [
            'reddit', 'medium', 'blogspot', 'wordpress', 
            'seekingalpha', 'benzinga', 'yahoo', 'pypi.org',
            'github.com', 'stackoverflow', 'medium.com',
            'timesofindia.indiatimes.com', 'onefootball.com',  # Add these
            'commondreams.org', 'staradvertiser.com'  # And these
        ]
        
        # Structure the news data
        news_items = []
        
        # Keywords that indicate AI is the main topic
        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'neural network',
            'openai', 'anthropic', 'chatgpt', 'claude', 'gemini', 'copilot',
            'llm', 'language model', 'generative', 'gpt', 'deepmind', 'moltbot'
        ]
        
        for article in articles:
            url = article.get('url', '').lower()
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            # Skip if from excluded source
            if any(source in url for source in excluded_sources):
                continue
            
            # Check if AI is mentioned in title OR description
            has_ai_content = any(keyword in title or keyword in description for keyword in ai_keywords)
            
            if not has_ai_content:
                continue
                
            news_items.append({
                'title': article.get('title', 'No title'),
                'description': article.get('description', 'No description'),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', '')
            })
        
        # Limit to 20 articles
        news_items = news_items[:20]
        
        print(f"✅ Found {len(news_items)} articles")
        
        return news_items
        
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test the collector
    print("Testing AI News Collector\n")
    print("="*70)
    
    news = get_ai_news()
    
    if news:
        print(f"\nFetched {len(news)} articles:\n")
        for i, item in enumerate(news[:10], 1):  # Show first 10
            print(f"{i}. {item['title']}")
            print(f"   Source: {item['source']}")
            print(f"   Description: {item['description'][:150]}...")  # First 150 chars
            print()