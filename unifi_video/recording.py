from __future__ import print_function, unicode_literals

from .single import UnifiVideoSingle
from datetime import datetime

endpoints = {
    'download': lambda x: 'recording/{}/download'.format(x),
}

class UnifiVideoRecording(UnifiVideoSingle):

    def _load_data(self, data):
        if not data:
            return

        self._data = data
        self._id = data['_id']
        self.rec_type = data.get('eventType', None)
        self.locked = data.get('locked', None)
        self.in_progress = data.get('inProgress', None)
        self.marded_for_deletion = data.get('markedForDeletion', None)
        self.cameras = data.get('cameras', [])
        self.start_time = datetime.fromtimestamp(
            int(data.get('startTime', 0) / 1000))
        self.end_time = datetime.fromtimestamp(
            int(data.get('endTime', 0) / 1000))

    def download(self, filename=None):
        return self._api.get(endpoints['download'](self._id),
            filename if filename else 'recording-{}-{}.mp4'.format(
                self._id, self.start_time.isoformat()))

    def __str__(self):
        return '{}: {}'.format(type(self).__name__, {
            '_id': self._id,
            'type': self.rec_type,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat()
        })
