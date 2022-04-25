const options = document.getElementById('options')
const table = document.getElementById("table");
const delete_id_item = document.getElementById('delete_id_item');

if(table !== null && delete_id_item !== null){
    table.addEventListener('click',(e) =>{
        if (e.target.innerHTML === 'Eliminar') 
            delete_id_item.value = e.target.id
    })
}

if(options!==null){
    options.addEventListener('click',(e)=>{
        if(e.target.id != null){
            console.log("entrando a evento")
            localStorage.setItem('current_id',e.target.id)
        }
    })
}

const next = () => {
    if(localStorage.getItem('current_ids') === null){
        if(localStorage.getItem('current_id') != null){
            console.log("entrando a next 1")
            localStorage.setItem('current_ids',localStorage.getItem('current_id'))
        }
    }else{
        if(localStorage.getItem('current_id') != null && localStorage.getItem('current_ids')){
            console.log("entrando a next 2")
            const temp = `${localStorage.getItem('current_ids')},${localStorage.getItem('current_id')}`
            localStorage.setItem('current_ids',temp)
        }
    }

    if(localStorage.getItem('current_ids') != null){
        const current_ids_input = document.getElementById('current_ids');
        current_ids_input.value = localStorage.getItem('current_ids');
    }
    localStorage.removeItem('current_id');
    //localStorage.clear()
}

const clean_local = () =>{
    localStorage.clear()
}
