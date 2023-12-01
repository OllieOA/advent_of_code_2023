from pathlib import Path
import shutil
import sys

DAYS_DIRECTORY = Path(__file__).parent / "days"
TEMPLATE_SOLVER = DAYS_DIRECTORY / "_template/solve_day.py"


def main():
    assert len(sys.argv) > 1, "You did not supply a day!"
    day = sys.argv[1]
    assert day.isdigit(), "You did not supply an integer!"
    day_num = int(day)
    assert day_num in range(1, 26), "Day is not an integer from 1-25!"

    day_directory = DAYS_DIRECTORY / f"day{day_num:02d}"
    assert not day_directory.exists(), "Day already exists!"

    day_directory.mkdir()
    files_to_make = [
        day_directory / "p1_sample.txt",
        day_directory / "p1_input.txt",
        day_directory / "p2_sample.txt",
        day_directory / "p2_input.txt",
    ]

    for file in files_to_make:
        file.touch()

    with open(TEMPLATE_SOLVER, "r") as f_in, open(day_directory / "solve_day.py", "w") as f_out:
        template = f_in.read()
        template = template.replace("DayX", f"Day{day_num:02d}")
        f_out.write(template)


if __name__ == "__main__":
    main()
