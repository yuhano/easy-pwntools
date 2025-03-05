#!/usr/bin/env python3
# main.py
import argparse
from elf_analyzer.analyzer import ELFAnalyzer
from elf_analyzer.printer import print_analysis_result, print_vulnerable_functions

def main():
    parser = argparse.ArgumentParser(description="Analyze ELF binaries and extract strings.")
    parser.add_argument("elf_file", help="Path to the ELF binary")
    parser.add_argument("--functions", nargs="*", help="List of function names to check vulnerability", default=None)
    args = parser.parse_args()

    analyzer = ELFAnalyzer(args.elf_file)
    analysis_result = analyzer.analyze()
    strings_file = analyzer.save_strings()
    analysis_result.strings_file = strings_file

    print_analysis_result(analysis_result)
    vuln_results = analyzer.check_vulnerable_functions(args.functions)
    print_vulnerable_functions(vuln_results)

if __name__ == "__main__":
    main()
