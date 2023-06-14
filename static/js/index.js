// This File defines vue reactivity for the index page

let app = {};

let init = (app) => {
    
    app.data = {

        // bools for toggling what html to display
        feed_mode:  true,
        add_mode:   false,
        view_mode:  false,
        mod_view:   false,

        popup_mode: false,

        // search variables
        search:         "",
        search_results: [],

        // list variables
        feed:           [],
        comments:       [], 

        // tag variables
        // tags:       [],
        // currentTag: "",

        // variables for add_story and add_comment variables
        add_title:    "",
        add_content:  "",
        add_author:   "",

        // view_story variables
        view_id:            -1,
        view_idx:           -1,
        view_title:         "",
        view_content:       "",
        view_author:        "",
        view_date:          "",
        view_likes:         -1,
        view_num_reports:   -1,
        view_reported_story: false,

        // mod vars
        ismod: false,
        report_view: false,
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
        // app.vue.add_tags    = "",
        // app.vue.tags        = [],

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
        // app.vue.add_tags    = "",
        // app.vue.tags        = [],

        // togle html view
        app.vue.feed_mode   = false;
        app.vue.add_mode    = false;
        app.vue.view_mode   = true;
    }

    app.view = (_idx) => {

        // get story details for viewing
        app.vue.view_id             = app.vue.feed[_idx].id;
        app.vue.view_idx            = app.vue.feed[_idx].id;
        app.vue.view_title          = app.vue.feed[_idx].title;
        app.vue.view_content        = app.vue.feed[_idx].content;
        app.vue.view_author         = app.vue.feed[_idx].author;
        app.vue.view_date           = app.vue.feed[_idx].creation_date;
        app.vue.view_likes          = app.vue.feed[_idx].likes;
        app.vue.view_num_reports    = app.vue.feed[_idx].num_reports;
        app.vue.view_reported_story = app.vue.feed[_idx].reported_story;

        // get comment list for viewing
        if (!app.vue.ismod || !app.vue.report_view)
            {app.get_comments();}
        else
            {app.get_rcomments();}

        app.set_view_mode();
        console.log("viewing", app.vue.view_title);
    }

    app.reset_search = () => {
        app.vue.search = "";
        app.vue.search_results = [];
        app.get_feed();
    }

    app.add_story = () => {
        axios.post(add_story_url, {
            title:      app.vue.add_title,
            content:    app.vue.add_content,
            // tags:       app.vue.tags,
        }).then((r) => {
            console.log("story", app.vue.add_title, "added");
            // app.vue.tags = []; // clear tags
            app.get_feed(); // only really need the id for the new story
            app.set_feed_mode();
        }).catch(() => {console.error("DEAD ADD_STORY");})
    };

    app.add_comment = () => {
        axios.post(add_comment_url, {
            content:    app.vue.add_content,
            story_id:   app.vue.view_id,
        }).then((r) => {
            
            app.get_feed(); // we just need to update 1 number, but it works

            console.log("comment added");
            app.vue.add_content = ""; // clear input fields
            app.get_comments() // refresh comments dynamically
        }).catch(() => {console.error("DEAD ADD_COMMENT");})
    };

    app.like_post = () =>{

    };

    // app.addTag = () => {
    //     let tag = app.vue.currentTag.trim();
    //     if (tag && app.vue.tags.indexOf(tag) < 0) {
    //         app.vue.tags.push(tag);
    //     }
    //     app.vue.currentTag = "";
    // };

    // app.removeTag = (index) => {
    //     app.vue.tags.splice(index, 1);
    // };

    app.get_feed = (search) => {
        axios.post(get_feed_url, { search: search })
            .then((r) => {
                app.vue.feed = app.enumerate(r.data.feed);
                console.log("Feed Loaded:", r.data.feed);
            })
            .catch(() => {
                console.error("DEAD GET_FEED");
            });

            app.vue.report_view = false; // disable report view
    }    

    app.get_comments = () => {
        axios.post(get_comments_url, {
            story_id:   app.vue.view_id, // assumes that a story is viewed
        }).then((r) => {
            app.vue.comments = app.enumerate(r.data.comments);
            console.log("comments loaded");
        }).catch(() => {console.error("DEAD GET_COMMENTS");})
    }

    app.report_story = () => {
        // assume user is viewing the story to use view variables
        axios.post(report_story_url, {
            story_id:       app.vue.view_id,
        }).then((r) => {
            app.open_popup();
            console.log("reported", app.vue.view_title,);
        }).catch(() => {console.error("DEAD REPORT_STORY");})
    }

    app.report_comment = (comment_id) => {
        // assume user is viewing the story to use view variables
        axios.post(report_comment_url, {
            story_id:         app.vue.view_id,
            comment_id:       comment_id, // passed in
        }).then((r) => {
            app.open_popup();
            console.log("reported comment", comment_id);
        }).catch(() => {console.error("DEAD REPORT_COMMENT");})
    }

    app.get_rfeed     = () => {
        axios.post(get_rfeed_url)
        .then((r) => {
            app.vue.feed = app.enumerate(r.data.reports);
            console.log("rfeed Loaded:", r.data.feed);
        })
        .catch(() => {
            console.error("DEAD GET_RFEED");
        });
        
        app.vue.report_view = true; // enable report view
    }

    app.get_rcomments = () => {
        axios.post(get_rcomments_url, {
            story_id:   app.vue.view_id, // assumes that a story is viewed
        }).then((r) => {
            app.vue.comments = app.enumerate(r.data.comments);
            console.log("rcomments loaded");
        }).catch(() => {console.error("DEAD GET_RCOMMENTS");})
    }

    app.get_ismod = () => {
        axios.post(get_ismod_url)
        .then((r) => {
            app.vue.ismod = r.data.ismod;
            console.log("ismod:", app.vue.ismod);
        })
        .catch(() => {console.error("DEAD ISMOD");});
    }

    app.approve_story = () => {
        axios.post(approve_story_url, {
            story_id:   app.vue.view_id,
        }).then((r) => {
            console.log("approved", app.vue.view_title);
            app.get_rfeed(); // refresh reported feed
            })
        .catch(() => {console.error("DEAD APPROVE_STORY");});
    }

    app.approve_comment = (comment_id) => {
        axios.post(approve_comment_url, {
            story_id:   app.vue.view_id,
            comment_id: comment_id,
        }).then((r) => {
            console.log("approved a comment on", app.vue.view_title);
            app.get_rcomments();
            app.get_rfeed();
            })
        .catch(() => {console.error("DEAD APPROVE_COMMENT");});
    }

    app.delete_story    = () => {
        axios.post(delete_story_url, {
            story_id:   app.vue.view_id,
        }).then((r) => {
            console.log("deleted", app.vue.view_title);
            app.get_rfeed(); // refresh reported feed

            app.set_feed_mode(); // go back to feed, because the story is gone
            })
        .catch(() => {console.error("DEAD DELETE_STORY");});
    }

    app.delete_comment  = (comment_id) => {
        axios.post(delete_comment_url, {
            story_id:   app.vue.view_id,
            comment_id: comment_id,
        }).then((r) => {
            console.log("deleted comment on ", app.vue.view_title);
            app.get_rcomments();
            app.get_rfeed();
            app.set_feed_mode(); // go back to feed, because the story is gone
            })
        .catch(() => {console.error("DEAD DELETE_STORY");});
    }

    app.open_popup    = () => {
        app.vue.popup_mode = true;
    }

    app.close_popup = () => {
        app.vue.popup_mode = false;
    }

    
    app.methods = {
        // mode switch methods
        set_feed_mode:      app.set_feed_mode,
        set_add_mode:       app.set_add_mode,
        set_view_mode:      app.set_view_mode,
        reset_search:       app.reset_search,

        // story functions
        add_story:          app.add_story,
        get_feed:           app.get_feed, // gets a list of stories
        view:               app.view,
        // addTag:          app.addTag,
        // removeTag:       app.removeTag,

        // comment functions
        add_comment:        app.add_comment,
        get_comments:       app.get_comments, // gets a list of comments


        // mod/admin regulation functions
        report_story:       app.report_story,
        report_comment:     app.report_comment,
        
        get_rfeed:          app.get_rfeed,
        get_rcomments:      app.get_rcomments,
        get_ismod:          app.get_ismod,

        // TODO functions
        approve_story:      app.approve_story,
        approve_comment:    app.approve_comment,

        delete_story:       app.delete_story,
        delete_comment:     app.delete_comment,

        // misc
        open_popup:       app.open_popup,
        close_popup:      app.close_popup,


    };
    
    app.vue = new Vue({
        el:      "#vue-target",
        data:    app.data,
        methods: app.methods,
    });
    
    app.init = () => {
        app.get_ismod();
        console.log("index.js Loaded");
        app.get_feed();
    };

    app.init();
};

init(app);
