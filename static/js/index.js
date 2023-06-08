// This File defines vue reactivity for the index page

let app = {};

let init = (app) => {
    
    app.data = {

        // bools for toggling what html to display
        feed_mode:      true,
        add_mode:       false,
        view_mode:      false,

        // list variables
        feed:           [],
        comments:       [],

        // variables for add_story and add_comment variables
        add_title:      "",
        add_content:    "",
        add_author:     "",

        // view_story variables
        view_id:        -1,
        view_title:     "",
        view_content:   "",
        view_author:    "",
        view_date:      "",

        // reply variables
        
    };
    
    app.enumerate = (a) => { // This adds an _idx field.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_feed_mode = () => {
        // togle html view
        app.vue.view_mode   = false;
        app.vue.add_mode    = false;
        app.vue.feed_mode   = true;
    }

    app.set_add_mode = () => {

        // reset the input fields for add_story input
        app.vue.add_title   = "",
        app.vue.add_content = "",
        app.vue.add_author  = "",

        // togle html view
        app.vue.feed_mode   = false;
        app.vue.view_mode   = false;
        app.vue.add_mode    = true;
    }

    app.set_view_mode = () => {

        // reset the input fields for add_comment input
        app.vue.add_title   = "",
        app.vue.add_content = "",
        app.vue.add_author  = "",

        // togle html view
        app.vue.feed_mode   = false;
        app.vue.add_mode    = false;
        app.vue.view_mode   = true;
    }

    app.view = (_idx) => {

        // get story details for viewing
        app.vue.view_id         = app.vue.feed[_idx].id;
        app.vue.view_title      = app.vue.feed[_idx].title;
        app.vue.view_content    = app.vue.feed[_idx].content;
        app.vue.view_author     = app.vue.feed[_idx].author;
        app.vue.view_date       = app.vue.feed[_idx].creation_date;

        // get comment list for viewing
       app.get_comments();

        app.set_view_mode();
        console.log("viewing", app.vue.view_title);
    }

    app.add_story = () => {
        axios.post(add_story_url, {
            title:      app.vue.add_title,
            content:    app.vue.add_content,
        }).then((r) => {
            console.log("story", app.vue.add_title, "added");
            app.get_feed(); // only really need the id for the new story
            app.set_feed_mode();
        }).catch(() => {console.error("DEAD ADD_STORY");})
    };

    app.add_comment = () => {
        axios.post(add_comment_url, {
            content:    app.vue.add_content,
            story_id:   app.vue.view_id,
            num_comments: app.vue.num_comments, 
        }).then((r) => {
            app.vue.num_comments += 1;
            console.log("comment added");
            app.vue.add_content = ""; // clear input fields
            app.get_comments() // refresh comments dynamically
        }).catch(() => {console.error("DEAD ADD_COMMENT");})
    };

    app.get_feed = () => {
        axios.post(get_feed_url).then((r) => {
            app.vue.feed = app.enumerate(r.data.feed);
            console.log("Feed Loaded:", r.data.feed);
        }).catch(() => {console.error("DEAD GET_FEED");})
    }

    app.get_comments = () => {
        axios.post(get_comments_url, {
            story_id:   app.vue.view_id, // assumes that a story is viewed
        }).then((r) => {
            app.vue.comments = app.enumerate(r.data.comments);
            console.log("comments loaded");
        }).catch(() => {console.error("DEAD GET_COMMENTS");})
    }

    app.report_post = () => {
        // TODO
        console.error("TODO: report_post js");
    }
    
    app.methods = {
        // mode switch methods
        set_feed_mode:  app.set_feed_mode,
        set_add_mode:   app.set_add_mode,
        set_view_mode:  app.set_view_mode,

        // story functions
        add_story:      app.add_story,
        get_feed:       app.get_feed, // gets a list of stories
        view:           app.view,

        // comment functions
        add_comment:    app.add_comment,
        get_comments:   app.get_comments, // gets a list of comments
        report_post:    app.report_post,
    };
    
    app.vue = new Vue({
        el:      "#vue-target",
        data:    app.data,
        methods: app.methods,
    });
    
    app.init = () => {
        console.log("index.js Loaded");
        app.get_feed();
    };

    app.init();
};

init(app);
