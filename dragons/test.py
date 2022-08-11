import sys
import subprocess

PHASE_PART_MAP = {
    "phase_1": {
        1: (1, 2),
        2: (3,),
        3: (4, 5)
    },
    "phase_2": {
        1: (1, 2, 3, 4),
        2: (5, 6),
        3: (7, 8),
        4: (9, 10)
    },
    "phase_3": {
        1: (1, 2),
        2: (3, 4, 5),
        3: (6, 7, 8)
    },
    "phase_4": {
        1: (1, 2),
        2: (3, 4, 5, 6),
        3: (7, 8, 9, 10),
        4: (11,),
        5: (12, 13)
    }
}


def invoke_ok(phase, suite=None):
    if suite is not None:
        cmd = [sys.executable, "ok", "-q", f"{phase}", "--suite", f"{suite}"]
    else:
        cmd = [sys.executable, "ok", "-q", f"{phase}", "--local"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    return stdout


def main(phases):
    details = get_phase_details(phases)
    print(details)
    for key, value in details.items():
        if -1 in value:
            result = run_tests(phase=key)
        else:
            result = run_tests(phase=key, value=value)
        if not result:
            break


def run_tests(phase, value=None):
    if value is None:
        print("*" * 69)
        print(f"STARTED RUNNING TESTS FOR {phase}")
        stdout = invoke_ok(phase)
        print(stdout)
        if stdout.find("# Error: expected") != -1:
            return False
        print(f"COMPLETED RUNNING TESTS FOR {phase}")
        print("*" * 69)
    else:
        for each in value:
            suite_numbers = PHASE_PART_MAP[phase][each]
            for suite in suite_numbers:
                print("*" * 69)
                print(f"STARTED RUNNING TESTS FOR {phase}, suite {suite}")
                stdout = invoke_ok(phase, suite)
                print(stdout)
                if stdout.find("# Error: expected") != -1:
                    return False
                print(f"COMPLETED RUNNING TESTS FOR {phase}, suite {suite}")
                print("*" * 69)
    return True


def get_phase_details(phases):
    from collections import defaultdict
    details = defaultdict(lambda: [])
    for each in phases:
        if each in PHASE_PART_MAP:
            details[each].append(-1)
        if "." in each:
            phase, part = each.split(".")
            if phase not in PHASE_PART_MAP:
                continue
            details[phase].append(int(part))
    return details


if __name__ == '__main__':
    _phases = sys.argv[1:]
    _phases = ["phase_" + phase.strip() for phase in _phases if phase.strip()]
    main(_phases)
