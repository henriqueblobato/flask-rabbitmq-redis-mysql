from redis import Redis


class RedisAdapter(Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
