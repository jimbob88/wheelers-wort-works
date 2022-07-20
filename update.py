def update():
    base_url = "https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master"
    files = {
        'beer_engine.py': f'{base_url}/beer_engine.py',
        'brew_data.py': f'{base_url}/brew_data.py',
        'main.py': f'{base_url}/main.py',
        'ScrolledWidgets.py': f'{base_url}/ScrolledWidgets.py',
        'AutoScroll.py': f'{base_url}/AutoScroll.py',
        'database.py': f'{base_url}/database.py',
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
