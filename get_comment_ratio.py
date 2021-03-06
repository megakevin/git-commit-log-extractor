# Usage: $ python3 get_comment_ratio.py /home/kevin/Desktop/sac-data/stats output.csv
#          python3 get_comment_ratio.py <merged_files> <output_path>
#
# Merges all the extracted contribution per tag data into one single file.

__author__ = 'kevin'

import sys
import csv
import os

# RQ 1: Generate a csv file for each project with: file, release, if its SAC, LOC
csv_header = ['project',
              'mean SAC', 'mean non SAC', "mean change",
              'median SAC', 'median non SAC', "median change",
              'pVal']

def median(l):
    l = sorted(l)
    if len(l) % 2 == 0:
        n = len(l)//2
        try:
            val = (l[n]+l[n-1])/2
        except Exception as ex:
            print(ex)

        return val
    else:
        return l[len(l)//2]

def mean(l):
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')

def main(argv):

    data_dir = argv[1]
    output_file = argv[2]

    result = []

    for data_file in os.listdir(data_dir):
        with open(os.path.join(data_dir, data_file), newline="") as csv_file:
            #file_name	lines_count	top_single_dev_contribution_knowledge
            # top_single_dev_contribution_knowledge_percent	commit_num	bug_commit_num
            # bug_commit_ratio	CountLine	CountLineCode	CountLineComment	SumCyclomatic

            # try:
            #     data = [{ 'contrib_percent': float(row['top_single_dev_contribution_knowledge_percent']),
            #               'count_line': float(row['CountLine'])}
            #             for row in csv.DictReader(csv_file)]
            # except Exception as ex:
            #     print(ex)

            data = [{ 'contrib_percent': float(row['top_single_dev_contribution_knowledge_percent']),
                      'count_line': float(row['lines_count']) if row['lines_count'] else 0,
                      'count_line_comment': float(row['CountLineComment']) if row['CountLineComment'] else 0,
                      'file_name': row['file_name']}
                    for row in csv.DictReader(csv_file)]

            files_sac = [{'count_line': l['count_line'],
                          'count_line_comment': l['count_line_comment']}
                         for l in data if l['contrib_percent'] >= 90]
            files_non_sac = [{'count_line': l['count_line'],
                              'count_line_comment': l['count_line_comment'],
                              'file_name': l['file_name']}
                             for l in data if l['contrib_percent'] < 90]

            # if any(l for l in files_sac if l['count_line'] == 0):
            #     print(files_sac)
            #
            # if any(l for l in files_non_sac if l['count_line'] == 0):
            #     print(files_sac)

            comment_ratios_sac = [(f['count_line_comment'] / f['count_line']
                                   if f['count_line'] else 0) * 100 for f in files_sac]
            comment_ratios_non_sac = [(f['count_line_comment'] / f['count_line']
                                       if f['count_line'] else 0) * 100 for f in files_non_sac]

            # if not comment_ratios_sac:
            #     print(comment_ratios_sac)
            #
            # if not comment_ratios_non_sac:
            #     print(comment_ratios_non_sac)

            mean_sac = mean(comment_ratios_sac)
            mean_non_sac = mean(comment_ratios_non_sac)

            mean_change = mean_non_sac - mean_sac

            median_sac = median(comment_ratios_sac)
            median_non_sac = median(comment_ratios_non_sac)

            median_change = median_non_sac - median_sac

        result.append({
            'project': data_file,
            'mean SAC': round(mean_sac, 2),
            'mean non SAC': round(mean_non_sac, 2),
            'mean change': round(mean_change, 2),
            'median SAC': round(median_sac, 2),
            'median non SAC': round(median_non_sac, 2),
            'median change': round(median_change, 2),
            'pVal': "TO CALCULATE"
        })

    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    main(sys.argv)
