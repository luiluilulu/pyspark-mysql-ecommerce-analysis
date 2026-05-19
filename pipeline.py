import argparse
import sys
import subprocess

STEPS = ['clean','ads','vis']

def run_step(step_name):

    command = {
        "clean":[sys.executable,"-m","etl.clean_user_behavior"],
        'ads' : [sys.executable,"-m","ads.build_ads"],
        'vis' : [sys.executable,'-m','viz.visualize_analysis']
    }
    cmd = command[step_name]
    print(f"\n{'='*40}")
    print(f"[START] {step_name}")
    result = subprocess.run(cmd)

    if result.returncode ==0:
        print(f"[DONE] {step_name}")
        return True
    else:
        print(f"[FATL] {step_name}")
        return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--step",choices=["all"]+STEPS,default="all")
    args = parser.parse_args()

    if args.step == "all":
        steps_to_run = STEPS
    else:
        steps_to_run = [args.step]

    for step in steps_to_run:
        ok = run_step(step)
        if not ok:
            print(f"\n!!!Pipeline在[{step}]失败,已终止")
            sys.exit(1)

    print(f"\nPipeline 全部完成")