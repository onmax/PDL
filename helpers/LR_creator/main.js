function inputChanged() {
    const str = (document.getElementById('input')).value
    const regex = /i\d+\s?=\s?{(.*?)\n}/gms

    let m

    let results = []

    while ((m = regex.exec(str)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }

        m.forEach(match => {
            if (match.substring(0, 1) === 'i')
                results.push(match)
        });
    }

    let statusDiv = document.querySelector('.status')

    results.map(r => {
        status = r.split("=")[0]
        options = r.split("\n")
        options.splice(0, 1)
        options.splice(-1, 1)
        options = options.map(o => o.split('-')).map(o => o.map(oo => oo.trim()))

        let parent = document.createElement('div')

        let bigBox = document.createElement('div')
        bigBox.className = 'big-box'

        options.map(o => {
            let div = document.createElement('div')
            div.innerHTML = `${o[0]} -> ${o[1]}`
            bigBox.appendChild(div)
        })

        let statusBox = document.createElement('div')
        statusBox.className = 'status-box'
        statusBox.innerHTML = status

        parent.appendChild(bigBox)
        parent.appendChild(statusBox)

        statusDiv.appendChild(parent)


    })


}