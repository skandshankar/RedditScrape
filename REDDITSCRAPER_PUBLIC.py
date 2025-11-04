"""
Reddit Scraper with Text-to-Speech Converter
Automates content gathering for Reddit content creators with TTS audio generation.

Requirements: praw, gtts
"""

import os
import string
import re
from gtts import gTTS
import praw


def sanitize_filename(filename, max_length=100):
    """
    Sanitize a string to be safe for use as a filename.

    Args:
        filename: String to sanitize
        max_length: Maximum length of the filename

    Returns:
        Sanitized filename string
    """
    # Remove invalid filename characters
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized = ''.join(c for c in filename if c in valid_chars)
    # Replace spaces with underscores and remove multiple spaces
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    # Limit length
    return sanitized[:max_length]


def create_output_directory(directory="audio_output"):
    """
    Create output directory if it doesn't exist.

    Args:
        directory: Name of the directory to create

    Returns:
        Path to the directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output directory: {directory}")
    return directory


def authenticate_reddit():
    """
    Authenticate with Reddit API using PRAW.

    Returns:
        Authenticated Reddit instance or None if authentication fails
    """
    try:
        reddit = praw.Reddit(
            client_id='stpzhsW96nKKuw',
            client_secret='6OLTWSaiwQfla8qPA4O-Vn_b_Gs',
            user_agent='TTS Scraper for reddit',
            username='botbottybotter',
            password='botterbot123'
        )
        # Test authentication
        reddit.user.me()
        print("✓ Login successful")
        return reddit
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return None


def get_user_input():
    """
    Get user preferences for scraping.

    Returns:
        Tuple of (subreddit_name, limit, sort_type, time_filter)
    """
    print("\n" + "="*50)
    print("Reddit TTS Scraper")
    print("="*50)

    # Get subreddit
    subreddit_name = input("\nEnter subreddit name (e.g., 'AskReddit'): ").strip()
    if not subreddit_name:
        print("✗ Subreddit name cannot be empty")
        return None

    # Get number of posts
    try:
        limit = int(input("Enter number of posts to fetch (1-100): ").strip())
        if limit < 1 or limit > 100:
            print("✗ Please enter a number between 1 and 100")
            return None
    except ValueError:
        print("✗ Invalid number")
        return None

    # Get sort type
    print("\nSort options:")
    print("1. Hot")
    print("2. Top")
    print("3. New")
    print("4. Rising")
    sort_choice = input("Select sort type (1-4, default: 2): ").strip() or "2"

    sort_map = {"1": "hot", "2": "top", "3": "new", "4": "rising"}
    sort_type = sort_map.get(sort_choice, "top")

    # Get time filter for 'top' posts
    time_filter = "all"
    if sort_type == "top":
        print("\nTime filter for 'top' posts:")
        print("1. All time")
        print("2. Year")
        print("3. Month")
        print("4. Week")
        print("5. Day")
        time_choice = input("Select time filter (1-5, default: 1): ").strip() or "1"
        time_map = {"1": "all", "2": "year", "3": "month", "4": "week", "5": "day"}
        time_filter = time_map.get(time_choice, "all")

    return subreddit_name, limit, sort_type, time_filter


def fetch_posts(reddit, subreddit_name, limit, sort_type, time_filter):
    """
    Fetch posts from a subreddit.

    Args:
        reddit: Authenticated Reddit instance
        subreddit_name: Name of the subreddit
        limit: Number of posts to fetch
        sort_type: Type of sorting (hot, top, new, rising)
        time_filter: Time filter for 'top' posts

    Returns:
        List of submissions or None if error
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)

        # Get posts based on sort type
        if sort_type == "hot":
            posts = subreddit.hot(limit=limit)
        elif sort_type == "top":
            posts = subreddit.top(time_filter=time_filter, limit=limit)
        elif sort_type == "new":
            posts = subreddit.new(limit=limit)
        elif sort_type == "rising":
            posts = subreddit.rising(limit=limit)
        else:
            posts = subreddit.top(limit=limit)

        return list(posts)

    except Exception as e:
        print(f"✗ Error fetching posts: {e}")
        return None


def generate_audio(submission, output_dir, language='en'):
    """
    Generate audio file from submission text.

    Args:
        submission: Reddit submission object
        output_dir: Directory to save audio file
        language: Language code for TTS

    Returns:
        Path to generated audio file or None if error
    """
    try:
        # Combine title and body text
        text = f"{submission.title}. {submission.selftext}"

        # Skip if no text content
        if not text.strip():
            print(f"  ⚠ Skipping (no text content)")
            return None

        # Create safe filename using submission ID and sanitized title
        safe_title = sanitize_filename(submission.title, max_length=50)
        filename = f"{submission.id}_{safe_title}.mp3"
        filepath = os.path.join(output_dir, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"  ⚠ File already exists, skipping")
            return filepath

        # Generate TTS audio
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filepath)

        return filepath

    except Exception as e:
        print(f"  ✗ Error generating audio: {e}")
        return None


def process_submissions(posts, output_dir):
    """
    Process list of Reddit submissions and generate audio files.

    Args:
        posts: List of Reddit submission objects
        output_dir: Directory to save audio files

    Returns:
        Number of successfully processed posts
    """
    successful = 0

    print(f"\n{'='*50}")
    print(f"Processing {len(posts)} posts...")
    print(f"{'='*50}\n")

    for i, submission in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {submission.title[:60]}...")
        print(f"  Author: u/{submission.author} | Score: {submission.score}")

        # Display text preview
        text_preview = submission.selftext[:100].replace('\n', ' ')
        if text_preview:
            print(f"  Text: {text_preview}...")

        # Generate audio
        filepath = generate_audio(submission, output_dir)

        if filepath:
            print(f"  ✓ Saved: {os.path.basename(filepath)}")
            successful += 1

        print()  # Blank line between posts

    return successful


def main():
    """Main execution function."""
    # Authenticate with Reddit
    reddit = authenticate_reddit()
    if not reddit:
        return

    # Get user input
    user_input = get_user_input()
    if not user_input:
        return

    subreddit_name, limit, sort_type, time_filter = user_input

    # Create output directory
    output_dir = create_output_directory("audio_output")

    # Fetch posts
    print(f"\n⟳ Fetching {sort_type} posts from r/{subreddit_name}...")
    posts = fetch_posts(reddit, subreddit_name, limit, sort_type, time_filter)

    if not posts:
        print("✗ No posts found or error occurred")
        return

    # Process submissions
    successful = process_submissions(posts, output_dir)

    # Summary
    print(f"{'='*50}")
    print(f"Summary: {successful}/{len(posts)} posts successfully converted")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"{'='*50}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Operation cancelled by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
