// This File defines vue reactivity for the index page

let app = {};

let init = (app) => {
    
    app.data = {
        feed: [],
    };
    
    app.enumerate = (a) => { // This adds an _idx field to each element in a.
        let k = 0; 
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.view = (id) => {
        console.log("view", id);
        axios.post(view_url, {id: id,}).then((r) => {
            console.log("viewed")
        })
    }
    
    app.methods = {
        view: app.view,
    };
    
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });
    
    app.init = () => {
        console.log("index.js Loaded");
        axios.get(get_feed_url).then((r) => {
            app.vue.feed = app.enumerate(r.data.feed);
            console.log(r.data.feed);
            console.log("Feed Loaded");
        });
    };

    app.init();
};

init(app);
