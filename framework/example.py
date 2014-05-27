from framework import Framework

if __name__ == '__main__':
    def hello_world():
        return 'Hello World!'

    def greeting(name):
        return 'Hello ' + name + '!'

    def name(first, last):
        return 'Hello ' + first + ' ' + last + '!'

    framework = Framework()
    framework.add_url_rule('/helloworld/', hello_world)
    framework.add_url_rule('/greeting/<name>', greeting)
    framework.add_url_rule('/name/<first>/<last>', name)
    framework.run(port=8080)
