import os
import sys
import subprocess
import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
logger.info(f"Project root: {PROJECT_ROOT}")

# Paths to scripts
LITERATURE_RETRIEVER = os.path.join(PROJECT_ROOT, 'scripts', 'literature_retriever.py')
PAPER_ANALYZER = os.path.join(PROJECT_ROOT, 'scripts', 'paper_analyzer.py')
DATA_DIR = os.path.join(PROJECT_ROOT, 'web', 'data')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

def run_script(script_path, args):
    """Run a Python script with arguments"""
    cmd = [sys.executable, script_path] + args
    logger.info(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            logger.info(f"Script executed successfully: {script_path}")
            return True
        else:
            logger.error(f"Script failed: {script_path}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error running script {script_path}: {e}")
        return False

def update_literature():
    """Update literature data"""
    logger.info("Starting literature update process...")
    
    # Step 1: Run literature retriever
    logger.info("Step 1: Retrieving latest literature")
    retriever_args = [
        '--timeframe', '3months',
        '--output', os.path.join(DATA_DIR, 'improved_papers.json'),
        '--browser', 'edge'
    ]
    
    if not run_script(LITERATURE_RETRIEVER, retriever_args):
        logger.error("Literature retrieval failed. Aborting update.")
        return False
    
    # Step 2: Run paper analyzer
    logger.info("Step 2: Analyzing retrieved papers")
    analyzer_args = [
        '--input', os.path.join(DATA_DIR, 'improved_papers.json'),
        '--output', os.path.join(DATA_DIR, 'improved_analyzed_papers.json')
    ]
    
    if not run_script(PAPER_ANALYZER, analyzer_args):
        logger.error("Paper analysis failed. Aborting update.")
        return False
    
    logger.info("Literature update completed successfully!")
    return True

def main():
    """Main function"""
    start_time = datetime.datetime.now()
    logger.info(f"Update started at: {start_time}")
    
    success = update_literature()
    
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    logger.info(f"Update finished at: {end_time}")
    logger.info(f"Duration: {duration}")
    
    if success:
        logger.info("Update completed successfully!")
        sys.exit(0)
    else:
        logger.error("Update failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
