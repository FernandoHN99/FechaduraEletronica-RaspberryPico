from dir_motion_detector.motion_detector import MotionDetector

if __name__ == '__main__':
    pir_01 = MotionDetector(14, True)
    pir_01.start_pir()

