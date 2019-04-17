"""
A script that uses FCtrlA's RustyRegion code to display/edit XCS regions locally. The aim being to avoid the performance
limitations of running RustyRegions on Apollo. It takes two arguments, a csv file of ObsIDs and a boolean argument to
determine if the code deletes files afterwards.
"""
from RustyRegions import Observation
import sys
import os
from threading import Thread
from queue import Queue
import subprocess
from time import sleep

xcs_dir = "/lustre/scratch/astro/xcs/XMM_observations/"
xcs_img_dir = "data/{obs_id}/images/"
xcs_file_dir = "code/xapa/id_results/{obs_id}/"
image_files = ["{obs_id}-0.50-2.00keV-pn_merged_img.fits",
               "{obs_id}-0.50-2.00keV-mos1_merged_img.fits",
               "{obs_id}-0.50-2.00keV-mos2_merged_img.fits",
               "{obs_id}-0.50-2.00keVmerged_img.fits"]
files_files = ["final_class_regions_REDO.reg", "final_sigs_all.dat", "final_source_summaries.dat"]


class SCPWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            obs_id = self.queue.get()
            try:
                #
                file_grabber(obs_id)
            finally:
                self.queue.task_done()


def file_grabber(observation):
    img_names = [file.format(obs_id=observation) for file in image_files]
    img_cmd = r"scp {uname}@apollo.hpc.susx.ac.uk:{path}{img_path}{{\{imgs}\}} {obs_id}".format(uname=username,
                                                                                                path=xcs_dir,
                                                                                                img_path=xcs_img_dir.format(
                                                                                                    obs_id=observation),
                                                                                                imgs=','.join(
                                                                                                    img_names),
                                                                                                obs_id=observation)

    file_cmd = r"scp {uname}@apollo.hpc.susx.ac.uk:{path}{file_path}{{\{files}\}} {obs_id}".format(uname=username,
                                                                                                   path=xcs_dir,
                                                                                                   file_path=xcs_file_dir.format(
                                                                                                       obs_id=observation),
                                                                                                   files=','.join(
                                                                                                       files_files),
                                                                                                   obs_id=observation)
    subprocess.call(img_cmd, shell=True)
    subprocess.call(file_cmd, shell=True)
    sleep(5)


def make_dirs(observations):
    if not os.path.exists('obs_viewer_files'):
        os.mkdir('obs_viewer_files')
    os.chdir('obs_viewer_files')

    for obs in observations:
        if not os.path.exists(obs):
            os.mkdir(obs)
        if not os.path.exists(obs + "_modded"):
            os.mkdir(obs + "_modded")
        else:
            print("A modded {obs} directory already exists, exiting program!".format(obs=obs))
            sys.exit(1)


def cleanup(observations):
    for obs in observations:
        subprocess.call('rm -r {obs_id}'.format(obs_id=obs), shell=True)


def setup_downloads(observations):
    queue = Queue()
    for i in range(1):
        worker = SCPWorker(queue)
        worker.daemon = True
        worker.start()

    for obs in observations:
        queue.put(obs)

    while queue.unfinished_tasks > len(observations)-2:
        pass


if __name__ == '__main__':
    # Checks arguments are present
    if len(sys.argv) != 3:
        print('First argument should be a .csv of ObsIDs, second argument should be true or false.')
        sys.exit(1)

    # Checks if  arguments are of correct type
    if not os.path.exists(sys.argv[1]):
        print('That file does not exist!')
        sys.exit(1)
    if sys.argv[2].lower() != 'false' and sys.argv[2].lower() != 'true':
        print('Only True or False is accepted!')
        sys.exit(1)

    obs_file = str(sys.argv[1])
    clean = str(sys.argv[2])
    username = str(input("Apollo Username: "))

    # Reads observations from file, and strips newline operators.
    obs_ids = open(obs_file, 'r').readlines()
    obs_ids = [ident.split('\n')[0] for ident in obs_ids]
    make_dirs(obs_ids)

    setup_downloads(obs_ids)
    for obs in obs_ids:
        obs_obj = Observation(obs, im_path=obs, region_file="{}/final_class_regions_REDO.reg".format(obs))
        obs_obj.setup_image(stretch="sqrt")
        obs_obj.setup_regions()
        obs_obj.edit(for_msl=True, save_path=obs+"_modded", sources_path=obs, sig_path=obs)

    # Deletes images and files if the clean argument was true
    if clean.lower() == 'true':
        cleanup(obs_ids)

