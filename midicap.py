import sys
import time
import mido
import rtmidi
import datetime
import threading

OUTPUT_DIR = ''


class MidiCap(object):
    def __init__(self, writedir):
        self.__writedir = writedir
        self.__midiin = rtmidi.MidiIn()
        self.__midiin.set_callback(self.record)
        self.__mid = mido.MidiFile()
        self.__track = mido.MidiTrack()
        self.__mid.tracks.append(self.__track)
        self.__timeout = threading.Timer(10, self.save)

        while True:
            try:
                self.__midiin.open_port(0)
                print('listening...')
                break
            except rtmidi._rtmidi.RtMidiError:
                print('could not open port - waiting 10 seconds')
                time.sleep(10)

    def record(self, event, data=None):
        if self.__timeout and self.__timeout.is_alive():
            self.__timeout.cancel()
        message, deltatime = event
        if deltatime >= 10:
            deltatime = 0

        if message[0] != 254:
            miditime = int(
                round(
                    mido.second2tick(deltatime, self.__mid.ticks_per_beat,
                                     mido.bpm2tempo(120))))

            print('deltatime: ', deltatime, 'msg: ', message)

            if message[0] == 144:
                self.__track.append(
                    mido.Message('note_on',
                                 note=message[1],
                                 velocity=message[2],
                                 time=miditime))
            elif message[0] == 176:
                self.__track.append(
                    mido.Message('control_change',
                                 channel=1,
                                 control=message[1],
                                 value=message[2],
                                 time=miditime))
            elif message[0] == 128:
                self.__track.append(
                    mido.Message('note_off',
                                 note=message[1],
                                 velocity=message[2],
                                 time=miditime))
        del self.__timeout
        self.__timeout = threading.Timer(10, self.save)
        self.__timeout.start()

    def save(self):
        if len(self.__track) > 0:
            name = datetime.datetime.now().strftime("capture_%Y_%m_%d_%H%M%S")
            self.__mid.save(f'{self.__writedir}/{name}.mid')
            print("\nRecording saved as " + name)
        del self.__mid
        del self.__track

        self.__mid = mido.MidiFile()
        self.__track = mido.MidiTrack()
        self.__mid.tracks.append(self.__track)

    def close(self):
        self.__midiin.close_port()
        del self.__midiin


def main():
    if len(sys.argv) > 1:
        writedir = sys.argv[1]
        print(f'writing midi files to {writedir}')
    else:
        print('writing midi files to midicap directory')
        writedir = OUTPUT_DIR
    midicap = MidiCap(writedir)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        midicap.save()
        midicap.close()


if __name__ == "__main__":

    if not OUTPUT_DIR:
        print('must define an output directory in midicap.py')
        sys.exit()

    main()
