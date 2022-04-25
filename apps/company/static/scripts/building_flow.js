const options_flow = document.getElementById('options_flow')

if(options_flow!==null){
    options_flow.addEventListener('click',(e)=>{
        localStorage.setItem('current_id_flow',e.target.id)
    })
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