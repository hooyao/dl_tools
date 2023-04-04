#!/usr/bin/env python3

import getopt
import os
import re
import sys

language_exts = ['chs', 'cht', 'eng', 'ch', '英', '简', '繁', 'zh']
video_exts = ['mp4', 'mkv']
sub_exts = ['srt', 'ass']

episode_reg = re.compile(r's(?P<season>\d+)e(?P<episode>\d+)')


def main(argv):
    directory = os.path.curdir
    opts, args = getopt.getopt(argv, "d:")
    for opt, arg in opts:
        if opt == '-h':
            print('sub_renamer.py -d <input directory>, if -d is not specified, the current directory will be used.')
            sys.exit()
        elif opt in ("-d", "--dir"):
            # set the directory containing the video and subtitle files
            directory = arg

    # extract the season and episode number from the video file name token
    def extract_season_epicode(token: str) -> (bool, int, int):
        if match := episode_reg.match(token):
            return True, (match.group('season')), int(match.group('episode'))
        return False, 0, 0

    # find all the files with the specified extensions
    video_files = [f for f in os.listdir(directory) if len(tokens := f.split('.')) > 0 and tokens[-1] in video_exts]
    sub_files = [f for f in os.listdir(directory) if len(tokens := f.split('.')) > 0 and tokens[-1] in sub_exts]

    # loop through all files in the directory
    for video_file_name in video_files:
        video_file_name_tokens = video_file_name.lower().split('.')
        # extract the season and episode number from the video file name
        # iterate through the tokens and use the regex to find the season and episode number
        season = 0
        episode = 0
        # part = 1
        for token in video_file_name_tokens:
            vd_suc, vd_s, vd_e = extract_season_epicode(token)
            if vd_suc:
                season = vd_s
                episode = vd_e
                break

        for sub_file_name in sub_files[:]:
            sub_file_tokens = sub_file_name.lower().split('.')
            for token in sub_file_tokens:
                sub_suc, sub_s, sub_e = extract_season_epicode(token)
                if sub_suc:
                    if sub_s == season and sub_e == episode:
                        # get the subtitle file extension
                        _, sub_ext = os.path.splitext(sub_file_name)
                        if len(sub_file_tokens) > 1:
                            # get the sub file language extension
                            sub_lang_ext = sub_file_tokens[-2]
                            video_file_name_wo_ext, vd_ext = os.path.splitext(video_file_name)
                            if any(supported_lang_ext in sub_lang_ext for supported_lang_ext in language_exts):
                                target_sub_name = video_file_name_wo_ext + f'.{sub_lang_ext}' + sub_ext
                            else:
                                target_sub_name = video_file_name_wo_ext + sub_ext

                            os.rename(os.path.join(directory, sub_file_name),
                                      os.path.join(directory, target_sub_name))
                            sub_files.remove(sub_file_name)
                            break


if __name__ == "__main__":
    main(sys.argv[1:])
