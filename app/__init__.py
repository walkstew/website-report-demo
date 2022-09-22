import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .main import main


def create_report(write=True, deploy=False, page=None):
  main(stage_locally=write, write_to_s3=deploy)
