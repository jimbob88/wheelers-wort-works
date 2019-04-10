def update():
    files = {
        'beer_engine.py': 'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master/beer_engine.py',
        'beer_engine2.py': 'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master/beer_engine2.py',
        'brew_data.py': 'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master/brew_data.py',
        'main.py': 'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master/main.py',
    }

    for file, url in files.items():
        print('Updating {file} from {url}'.format(file=file, url=url))
        if sys.version_info >= (3, 0):
            with urlopen(url) as response, open(resource_path(file), 'wb') as out_file:
                data = response.read()
                out_file.write(data)
        else:
            response = urlopen(url)
            out_file = open(file, 'wb')
            data = response.read()
            out_file.write(data)

    if sys.version_info >= (3, 0):
        import beer_engine
    else:
        import beer_engine2 as beer_engine
