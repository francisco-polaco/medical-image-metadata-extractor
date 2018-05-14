#!/bin/bash
apt install -yqq python3-pip python3
pip3 install pydicom nibabel
echo
echo "Done! :)"
echo "Run the script using the following command: "
echo "python3 image.py [dicom|nifti] <filename>"
echo