const options_flow = document.getElementById('options_flow')
const result_flow = document.getElementById('inspection_result')

if(options_flow!==null){
    options_flow.addEventListener('click',(e)=>{
        localStorage.setItem('current_id_flow',e.target.id)
    })
}

function exists_id(id_actual){
    list_ids = localStorage.getItem('current_ids_final_flow')
    if(list_ids == null){
        localStorage.setItem('current_ids_final_flow',id_actual)
    }else{
        const split_id = list_ids.split(',')

        for (let i = 0; i < split_id.length; i++){
            if(id_actual != split_id[i]){
                const temp = `${list_ids},${id_actual}`
                localStorage.setItem('current_ids_final_flow',temp)
            }
        }
    }
}

if(result_flow!==null){
    result_flow.addEventListener("click",(e)=>{
        //localStorage.setItem('current_id_final_flow',e.target.id)
        //exists_id(e.target.id)
        id_actual = e.target.id
        list_ids = localStorage.getItem('current_ids_final_flow')
        if(list_ids == null){
            localStorage.setItem('current_ids_final_flow',id_actual)
        }else{
            const split_id = list_ids.split(',')
            //console.log(split_id)
            let exist_id = false
            let string_ids = ""

            for(let i = 0; i < split_id.length; i++){
                if(split_id[i] == id_actual){
                    exist_id = true
                    //split_id.splice(i,1)
                    break
                }

                if(exist_id == false){
                    if(string_ids == ""){
                        string_ids = split_id[i]
                    }else{
                        string_ids = string_ids + ',' + split_id[i]
                    }
                }
            }

            console.log(string_ids)
            console.log(exist_id)
            if(exist_id == false){
                const temp = `${string_ids},${id_actual}`
                localStorage.setItem('current_ids_final_flow',temp)
            }

            
        }
    })
}

const checking = () => {
    console.log("llamando checking")
    const current_ids_input = document.getElementById('ids_final_flow');
    current_ids_input.value = localStorage.getItem('current_ids_final_flow');
}

const next_flow = () => {
    if(localStorage.getItem('current_ids_flow') === null){
        localStorage.setItem('current_ids_flow',localStorage.getItem('current_id_flow'))
    }else{
        const temp = `${localStorage.getItem('current_ids_flow')},${localStorage.getItem('current_id_flow')}`
        localStorage.setItem('current_ids_flow',temp)
    }

    const current_ids_input = document.getElementById('current_ids_flow');
    current_ids_input.value = localStorage.getItem('current_ids_flow');

    //localStorage.clear()
}

/*ids = localStorage.getItem('current_id_final_flow')
        actual_id = e.target.id
        console.log(ids)
        if(ids === null){
            localStorage.setItem('current_id_final_flow',actual_id)
        }else{
            const list_id = ids.split(',')
            string_id = ""
            for (let i = 0; i < list_id.length; i++) {
                if(actual_id == list_id[i]){
                    list_id.splice(i,1)
                    break;
                }         

                if(string_id == ""){
                    string_id = list_id[i]
                }else{
                    string_id = string_id + ',' + list_id[i]
                }
            } 
            
            const temp = `${string_id},${e.target.id}`
            localStorage.setItem('current_id_final_flow',temp)
}*/