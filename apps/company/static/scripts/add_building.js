const options = document.getElementById('options')

options.addEventListener('click',(e)=>{
    localStorage.setItem('current_id',e.target.id)
})

const next = () => {
    if(localStorage.getItem('current_ids') === null){
        localStorage.setItem('current_ids',localStorage.getItem('current_id'))
    }else{
        const temp = `${localStorage.getItem('current_ids')},${localStorage.getItem('current_id')}`
        localStorage.setItem('current_ids',temp)
    }

    const current_ids_input = document.getElementById('current_ids');
    current_ids_input.value = localStorage.getItem('current_ids')
}
