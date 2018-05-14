import os
import pydicom
import sys
import nibabel as nib
import pprint
from pydicom.data import get_testdata_files

#pp = pprint.PrettyPrinter()

def myprint(dataset, indent=0):
    """Go through all items in the dataset and print them with custom format
    Modelled after Dataset._pretty_str()
    """
    dont_print = ['Pixel Data', 'File Meta Information Version']

    indent_string = "   " * indent
    next_indent_string = "   " * (indent + 1)

    for data_element in dataset:
        if data_element.VR == "SQ":   # a sequence
            print(indent_string, data_element.name)
            for sequence_item in data_element.value:
                myprint(sequence_item, indent + 1)
                print(next_indent_string + "---------")
        else:
            if data_element.name in dont_print:
                print("""<item not printed -- in the "don't print" list>""")
            else:
                repr_value = repr(data_element.value)
                if len(repr_value) > 50:
                    repr_value = repr_value[:50] + "..."
                print("{0:s} {1:s} = {2:s}".format(indent_string,
                                                   data_element.name,
                                                    repr_value))

def dicom_print(image_filename: str):
    if image_filename is None:
        image_filename = 'MR_small.dcm'
        print("Filename missing, using default file: MR_small.dcm")
        filename = get_testdata_files(image_filename)[0] 
    else:
        filename = image_filename
            
    ds = pydicom.dcmread(filename)
    myprint(ds)

def nifti_print(image_filename: str):
    if image_filename is None:
        image_filename = 'avg152T1_LR_nifti.nii.gz'
        print("Filename missing, using default file: avg152T1_LR_nifti.nii.gz")

    img = nib.load(image_filename)
    print(str(img.header))
    print("Shape\t\t: " + str(img.header.get_data_shape()))


def main():
    if len(sys.argv) > 1:
        image_format = sys.argv[1]
    else:
        print("Image format not passed. Usage: python3 image.py [dicom|nifti] <filename>")
        return -1
    
    if len(sys.argv) > 2:
        image_filename = sys.argv[2]
    else:
        image_filename = None

    if image_format == "dicom":
        dicom_print(image_filename)
    elif image_format == "nifti":
        nifti_print(image_filename)
    else:
        print("Image format unknown. Format passed: " + image_format)
        return -1

main()
