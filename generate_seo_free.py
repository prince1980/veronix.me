import os
import sys
import argparse
from seo_core.ai_provider import AIProvider
from seo_core.strategy_manager import get_existing_article_titles, evaluate_topic
from seo_core.research_pipeline import get_raw_knowledge, verify_claims_and_extract
from seo_core.article_generator import generate_draft, quality_gate_check, revise_draft
from seo_core.publishing_system import generate_metadata, apply_internal_links, save_article, update_index_and_sitemap

KNOWLEDGE_DIR = r"D:\workk\OUTPUT\OG OUTPUT\new style\Carson Clients\Project 6\Veronix Content"
DOCUMENTATION_DIR = "documentation"

def main():
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    parser = argparse.ArgumentParser(description="Veronix Content Operations System")
    parser.add_argument("--dry-run", action="store_true", help="Run the entire pipeline without uploading or saving files.")
    args = parser.parse_args()
    
    is_dry_run = args.dry_run
    
    print("\n\033[35m==================================================\033[0m")
    print("\033[1m VERONIX CONTENT OPERATIONS SYSTEM \033[0m")
    if is_dry_run:
        print("\033[33m [DRY RUN MODE ENABLED - NO FILES WILL BE SAVED] \033[0m")
    print("\033[35m==================================================\033[0m\n")
    
    ai_provider = AIProvider(max_retries=3)
    
    # 1. Gather existing context to prevent cannibalization
    print("\033[34m>\033[0m Scanning existing documentation to prevent keyword cannibalization...")
    existing_titles = get_existing_article_titles(DOCUMENTATION_DIR)
    
    max_topic_retries = 20
    strategy_eval = None
    verified_data = None
    proposed_topic = None
    
    for attempt in range(max_topic_retries):
        # 2. Extract Raw Knowledge
        print(f"\n\033[34m>\033[0m Pulling raw transcription data from internal knowledge base (Attempt {attempt+1}/{max_topic_retries})...")
        raw_data = get_raw_knowledge(KNOWLEDGE_DIR)
        if not raw_data:
            print("\033[31m>\033[0m \033[1mError: No valid knowledge files found in Veronix Content.\033[0m")
            sys.exit(1)
            
        print(f"\033[36m>\033[0m Selected source: {raw_data['source_file']}")
        
        # 3. Verify Claims and Extract Core Insights
        print("\033[34m>\033[0m Fact-checking transcript and stripping unverified numerical claims...")
        verified_data = verify_claims_and_extract(ai_provider, raw_data)
        if not verified_data:
            print("\033[33m>\033[0m \033[1mResearch extraction failed. Retrying...\033[0m")
            continue
            
        proposed_topic = verified_data.get('suggested_topic', 'Unknown Topic')
        print(f"\033[36m>\033[0m Proposed Topic: {proposed_topic}")
        
        # 4. Strategy Gate (Should We Publish?)
        print("\033[34m>\033[0m Running Strategy Gate Check (Cannibalization & Cluster Match)...")
        strategy_eval = evaluate_topic(ai_provider, proposed_topic, existing_titles)
        
        if not strategy_eval.get('approved', False):
            print("\n\033[31m========================================\033[0m")
            print("\033[31m \033[1mARTICLE REJECTED BY STRATEGY GATE\033[0m")
            print(f"\033[33m Reason: {strategy_eval.get('reason', 'Unknown')}\033[0m")
            print("\033[31m========================================\033[0m\n")
            continue
            
        print(f"\033[32m>\033[0m \033[1mApproved:\033[0m Fits into {strategy_eval.get('cluster', 'approved cluster')} cluster with no cannibalization.")
        
        # 5 & 6. Drafting & Quality Loop
        print("\033[34m>\033[0m Drafting authoritative article based purely on verified knowledge...")
        draft = generate_draft(ai_provider, verified_data['verified_context'], proposed_topic)
        
        if not draft:
            print("\033[33m>\033[0m Draft generation failed completely. Retrying with next source...")
            continue
            
        print("\033[34m>\033[0m Evaluating draft quality and EEAT signals...")
        quality = quality_gate_check(ai_provider, draft)
        score = quality.get('total_score')
        
        # Revision Loop
        max_revisions = 2
        for revision in range(max_revisions):
            if quality.get('passed', False):
                break
                
            if score is None:
                # API error during quality check
                break
                
            print(f"\033[33m>\033[0m Draft scored {score}/100. Revising draft based on feedback (Revision {revision+1}/{max_revisions})...")
            draft = revise_draft(ai_provider, draft, quality.get('feedback', 'Improve depth and originality.'))
            
            print("\033[34m>\033[0m Re-evaluating revised draft quality...")
            quality = quality_gate_check(ai_provider, draft)
            score = quality.get('total_score')
            
        if score is None:
            print("\033[33m>\033[0m \033[1mQuality check encountered an API error. Skipping to next topic.\033[0m")
            continue
            
        if not quality.get('passed', False):
            print("\n\033[31m========================================\033[0m")
            print(f"\033[31m \033[1mARTICLE REJECTED BY QUALITY GATE (Score: {score}/100)\033[0m")
            print(f"\033[33m Feedback: {quality.get('feedback', 'Too low quality')}\033[0m")
            print("\033[31m========================================\033[0m\n")
            print("\033[33m>\033[0m \033[1mArticle failed quality gate even after revisions. Skipping to next topic.\033[0m")
            continue
            
        print(f"\033[32m>\033[0m \033[1mQuality check passed (Score: {score}/100).\033[0m")
        
        # If we successfully passed all gates, break the main topic loop and proceed to publish!
        break
    
    if not strategy_eval or not strategy_eval.get('approved', False) or not quality or not quality.get('passed', False):
        print("\033[31m>\033[0m \033[1mCould not generate an approved, high-quality article after maximum retries. Exiting.\033[0m")
        sys.exit(0)
    
    # 7. Metadata & Publishing System
    print("\033[34m>\033[0m Generating internal links and Schema.org metadata...")
    metadata = generate_metadata(ai_provider, draft)
    draft['body_html'] = apply_internal_links(draft['body_html'], existing_titles)
    
    print("\n\033[35m================ PUBLISHING REVIEW ================\033[0m")
    print(f" TITLE   : {draft['title']}")
    print(f" SLUG    : {metadata.get('slug')}")
    print(f" CLUSTER : {strategy_eval.get('cluster')}")
    print(f" SCORE   : {score}/100")
    print(f" STATUS  : {'Ready for Publishing' if not is_dry_run else 'DRY RUN - NOT SAVED'}")
    print("\033[35m===================================================\033[0m\n")
    
    if not is_dry_run:
        slug = save_article(draft, metadata, is_dry_run)
        update_index_and_sitemap(draft, metadata, slug, is_dry_run)
        print("\033[32m>\033[0m \033[1mArticle written to disk.\033[0m")
        
        print(f"\033[34m>\033[0m \033[1mPushing to GitHub (origin/master)\033[0m")
        import subprocess
        subprocess.run(["git", "add", "documentation/", "sitemap.xml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        commit_res = subprocess.run(["git", "commit", "-m", "feat: auto-generated SEO article via AI"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if commit_res.returncode == 0:
            push_res = subprocess.run(["git", "push", "origin", "master"])
            if push_res.returncode == 0:
                print("\033[32m>\033[0m \033[1mSuccess: Article deployed successfully.\033[0m\n")
            else:
                print("\033[31m>\033[0m \033[1mError: GitHub push failed. Please check your git connection.\033[0m\n")
        else:
            print("\033[33m>\033[0m \033[1mNote: No new changes to commit. (Article was likely identical to an existing one)\033[0m\n")
    else:
        print("\033[33m>\033[0m Dry run completed successfully. No files were modified.\n")

if __name__ == "__main__":
    main()
