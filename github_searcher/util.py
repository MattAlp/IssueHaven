import time


def rate_limit_github(func, client):
    def wrapped():
        print(client.rate_limiting)
        if client.rate_limiting[0] <= 5:
            print("[INFO] Rate limit approached, sleeping until", time.ctime(client.rate_limiting_resettime))
            try:
                time.sleep(client.rate_limiting_resettime - time.time())
            except:
                pass
        return func
    return wrapped()
