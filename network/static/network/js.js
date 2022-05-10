var last_form = null;

document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('[id^="edit_form_"]').forEach(form => {
        
        form.onsubmit = function (e) {
            e.preventDefault();
            this.querySelector('#div_buttons').style.display = "none";
            var formData = $(this).serialize();
            let csrftoken = this.querySelector("input[name='csrfmiddlewaretoken']").value;
            fetch(`/edit/${this.dataset.id}`, {
                    method: 'POST',
                    headers: {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "X-CSRFToken": csrftoken
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    

                    console.log(data.result)
                    this.querySelector('#div_buttons').style.display = "";
                })
                let p = document.querySelector('#post_text_' + this.dataset.id);
            let form1 = document.querySelector('#edit_form_' + this.dataset.id);
            p.innerHTML  =form1.querySelector('#id_post_edit_text').value  ;
            
                hideform(form);
        }


    });
    document.querySelectorAll("[id^='like_']").forEach(a=>{
        a.onclick= function (e){
            e.preventDefault
            fetch(`/like/${this.dataset.id}`)            
            .then(response => response.json())
            .then(data => {
                console.log(data.count);
                document.querySelector('#like_count_'+this.dataset.id).innerHTML=data.count
                if (data.result==='removed')
                {
                    this.classList.remove("bg-dark");
                    this.classList.add('bg-white');
            };
            if (data.result==='added')
            {
                this.classList.remove("bg-white");
                this.classList.add('bg-dark');
        };
                
            })
        }
    })

    document.querySelectorAll("[id^='edit_link_']").forEach(a => {

        a.onclick = function () {
            if (last_form != null) {
                hideform(last_form);
                        console.log(this)
            }
            last_form = this;
            
            let p = document.querySelector('#post_text_' + this.dataset.id);
            let form = document.querySelector('#edit_form_' + this.dataset.id);
            p.style.display = 'none';
            form.querySelector('#id_post_edit_text').value = p.innerHTML;
            form.style.display = '';
            
        };

    });



    document.querySelectorAll("[id^='btn_close_']").forEach(a => {
        a.onclick = function () {
            hideform(this);
        };

    });
function hideform(element) {

    let p = document.querySelector('#post_text_' + element.dataset.id);
    console.log(p.innerHTML);

    let form = document.querySelector('#edit_form_' + element.dataset.id);
    p.style.display = '';
    console.log(form);
    // form.querySelector('#id_post_edit_text').value = p.innerHTML;
    form.style.display = 'none';

};

});