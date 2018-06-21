import time


def rate_limit_github(func, client):

    def wrapped():
        if client.rate_limiting[0] == 0:
            print(
                "[INFO] Rate limit exceeded, sleeping until ",
                client.rate_limiting_resettime,
            )
            try:
                time.sleep(client.rate_limiting_resettime - time.time())
            except:
                pass
        return func

    return wrapped()
