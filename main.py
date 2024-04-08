import sys
import os

# Get the directory containing your main.py file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Add the scripts directory to the Python path
sys.path.append(os.path.join(dir_path, 'scripts'))

from stage1_SubtitleExractor import subtitle_extracttor
from stage2_FeatureExtraction import feature_extraction
from stage3_PreprocessTrainTest import run

# Main function
def main():
    subtitle_extracttor()
    feature_extraction()
    run()