document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }


    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          if (this.currentStep === 3) {
            this.updateInstitution()
          }
          if (this.currentStep === 5) {
            this.getDataAndSummary()
          }
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }
    getDataAndSummary () {
      let data = this.getFormValue()
      let institutes = data.institution
      if (institutes) {
        let name_institute = institutes.nextElementSibling.nextElementSibling.children[0].innerText
        let form_institute = document.querySelector('.institute')
        form_institute.innerText = `Dla fundacji ${name_institute}`
      }

      let quantity = data.quantity
      let form_quantity = document.querySelector('.quantity')
      let info_bags = 'worków'
      if (quantity.value == 1) {
        info_bags = 'worek'
      } else if (quantity.value == '') {
        info_bags = '0 worków'
      }
      form_quantity.innerText = `Odajesz ${quantity.value} ${info_bags}`

      let address = data.address
      let city = data.city
      let zip_code = data.zipcode
      let phone_number = data.phone_number
      let form_address = document.querySelector('.form-address')
      if (address.value !== '' && city.value !== '' && zip_code.value !== '' && phone_number.value !== '') {
        form_address.innerHTML = `
          <li>${address.value}<li>
          <li>${city.value}<li>
          <li>${zip_code.value}<li>
          <li>${phone_number.value}<li>`
      } else {
        form_address.innerHTML = `
        <li>Uzupełnij dane dotyczące adresu</li>
        `
      }
      let date = data.date
      let time = data.time
      let comment = data.comment
      let form_delivery = document.querySelector('.form-delivery')
      if (date.value !== '' && time.value !== '' && comment.value !== '') {
        form_delivery.innerHTML = `
          <li>${date.value}<li>
          <li>${time.value}<li>
          <li>${comment.value}<li>\`
          `
      } else {
        form_delivery.innerHTML = `
        <li>Uzupełnij dane dotyczące terminu odbioru</li>
        `
      }
    }

    updateInstitution() {
      let categories = document.querySelectorAll('#categories')
      let categories_id = [];
      console.log(window.location.host)
      categories.forEach(el => {
        if (el.checked === true) {
          categories_id.push(el.value)
        }
      })
      fetch(`/categories/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFTOKEN': this.getCookie('csrftoken')
        },
        body: JSON.stringify({'categories_id': categories_id})})
          .then(response => response.json())
          .then(result => {
            let main = document.querySelector('div[data-step="3"]')
            main.innerHTML = ''
            let h3 = document.createElement('h3')
            h3.innerText = 'Wybierz organizacje, której chcesz pomóc:'
            main.appendChild(h3)
            if (result.response.length > 0) {
              result.response.forEach(el => {
                let div = document.createElement('div')
                div.classList.add('form-group', 'form-group--checkbox')
                let label = document.createElement('label')
                div.appendChild(label)
                let input = document.createElement('input')
                input.type = 'radio'
                input.name = 'organisation'
                input.value = el.id
                input.id = 'organisation'
                let span1 = document.createElement('span')
                span1.classList.add('checkbox', 'radio')
                label.appendChild(input)
                label.appendChild(span1)
                let span2 = document.createElement('span')
                span2.classList.add('description')
                let div_span2 = document.createElement('div')
                div_span2.classList.add('title')
                div_span2.innerText = el.name
                span2.appendChild(div_span2)
                let div2_span2 = document.createElement('div')
                div2_span2.classList.add('subtitle')
                div2_span2.innerText = el.description
                span2.appendChild(div2_span2)
                label.appendChild(span2)
                main.appendChild(div)
              })
            }
            else {
              let info_h3 = document.createElement('h3')
              info_h3.innerText = 'Żadna organizacja nie spełnia wymagań.'
              main.appendChild(info_h3)
            }
            let div_button = document.createElement('div')
              div_button.classList.add('form-group', 'form-group--buttons')
              let buttonPrev = document.createElement('button')
              buttonPrev.type = 'button'
              buttonPrev.classList.add('btn', 'prev-step')
              buttonPrev.innerText = 'Wstecz'
              buttonPrev.addEventListener('click', e => {
                e.preventDefault()
                this.currentStep--
                this.updateForm()
              })
              let buttonNext = document.createElement('button')
              buttonNext.type = 'button'
              buttonNext.classList.add('btn', 'next-step')
              buttonNext.innerText = 'Dalej'
              buttonNext.addEventListener('click', e => {
                e.preventDefault()
                this.currentStep++
                this.updateForm()
              })
              div_button.appendChild(buttonPrev)
              div_button.appendChild(buttonNext)
              main.appendChild(div_button)
          })
          .catch(error => {
        console.log(error)
          })
    }

    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue
    }

    getFormValue() {
      let institution = document.querySelector('[name="organisation"]:checked')
      let data = {
        'address': document.querySelector('[name="address"]'),
        'city': document.querySelector('[name="city"]'),
        'zipcode': document.querySelector('[name="postcode"]'),
        'phone_number': document.querySelector('[name="phone"]'),
        'date': document.querySelector('[name="date"]'),
        'time': document.querySelector('[name="time"]'),
        'comment': document.querySelector('[name="more_info"]'),
        'quantity': document.querySelector('[name="bags"]'),
        'institution': document.querySelector('[name="organisation"]:checked'),
        'categories': document.querySelectorAll('[name="categories"]:checked')
      }
      return data
    }

    sendForm () {
      let data = this.getFormValue()
      let categories = document.querySelectorAll('#categories')
      let categories_id = [];
      categories.forEach(el => {
        if (el.checked === true) {
          categories_id.push(el.value)
        }
      })
      let institution = 'error'
        if (data.institution !== null) {
          institution = data.institution.value
        }
      let form = {
        'address': data.address.value !== '' ? data.address.value: 'error',
        'city': data.city.value !== '' ? data.city.value : 'error',
        'zip_code': data.zipcode.value !== '' ? data.zipcode.value: 'error',
        'phone_number': data.phone_number.value !== '' ? data.phone_number.value: 'error',
        'pick_up_date': data.date.value !== '' ? data.date.value: 'error',
        'pick_up_time': data.time.value !== '' ? data.time.value: 'error',
        'pick_up_comment': data.comment.value !== '' ? data.comment.value: 'error',
        'quantity': data.quantity.value !== '' ? data.quantity.value: 'error',
        'institution': institution,
        'categories': categories_id
      }
      fetch(`/form-request/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFTOKEN': this.getCookie('csrftoken')
        },
        body: JSON.stringify({'form': form})})
          .then(response => response.json())
          .then(data => {
            if (data.response === "Data saved") {
              window.location.assign( `/form-confirmation/confirmed/`)
            } else {
              window.location.assign(`/form-confirmation/unconfirmed/`)
            }
          }).catch(error => {
            console.log(error)
      })
    }
    /**
     * Submit form
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
      this.sendForm()
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  /*
    Contact Form Submit
   */
  (function () {
    let buttonContact = document.querySelector('.form--contact > button')
    buttonContact.addEventListener('click', (event) => {
      event.preventDefault()
      let data = {
        'name': document.querySelector('#name').value,
        'surname': document.querySelector('#surname').value,
        'message': document.querySelector('#message').value
      }
      fetch('/form-contact-request/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'form': data})})
          .then(response => response.json())
          .then((data) => {
            console.log(data)
            const response = document.querySelector('.output > h3')
            if (data.response === "Data saved") {
              response.innerText = "Formularz przyjęty"
              console.log(event.target)
              event.target.disabled = true
            } else {
              response.innerText = "Nie poprawne dane w formularzu"
            }
          }).catch((error) => {
            console.log(error)
      })
    })
  })()


});
