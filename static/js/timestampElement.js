// Create a class for the element
class TimeElement extends HTMLElement {

    static observedAttributes = ["time"];
  
    constructor() {
      super();

      const shadow = this.attachShadow({ mode: "open" });
      const wrapper = document.createElement('div');
      const timeParagraph = document.createElement('p');
      
      wrapper.appendChild(timeParagraph);

      shadow.appendChild(wrapper);

    }
  
    //connectedCallback() {
    //    
    //}
  
    attributeChangedCallback(name, oldValue, newValue) {
        if (name == "time") {
            _render(newValue);
        }
    }

    _render(time) {
    }
  }
  
  customElements.define("time-element", TimeElement);
  