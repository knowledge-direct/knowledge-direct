//################## CONFIG ################
const SERVER_PREFIX = 'http://localhost:8080'
const GOOGLE_CLIENT_ID = "36026118361-bkpia5j1sh7t1sceg0o4jfsb299afv72.apps.googleusercontent.com";
const GOOGLE_CLIENT_SECRET = "G6PXs1PtDnEZQc6TF-9Le6Be";

const logger = require('./logger.js')

//######################## Initialise server ###############################
const restify = require('restify');
const sessions = require('client-sessions');
const server = restify.createServer({
    name: 'myapp',
    version: '1.0.0',
    log: logger
});
server.use(restify.acceptParser(server.acceptable));
server.use(restify.queryParser());
server.use(restify.bodyParser());
server.use(sessions({
    cookieName: 'session',
    secret: 'dfkslafjkdlsafjdksl;afjdkls;ajadfasklj',
    duration: 1000 * 60 * 60 // ms
}));

// ############## Authentication ########################
const passport = require('passport-restify');
const GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;


passport.use(new GoogleStrategy({
    clientID: GOOGLE_CLIENT_ID,
    clientSecret: GOOGLE_CLIENT_SECRET,
    callbackURL: 'http://localhost:8080/auth/google/callback',
    passReqToCallback: true
}, (request, accessToken, refreshToken, profile, done) => {
        console.log('google strategy call back')
        done(null, profile)
        //User.findOrCreate({ googleId: profile.id }, function (err, user){
            //return done(err, user);
        //});
}));

passport.serializeUser((user, done) => {
    logger.info('sererilise user')
    done(null, user);
});

passport.deserializeUser((user, done) => {
    logger.info('deserilise user')
    done(null, user);
});

server.use(passport.initialize());
server.use(passport.session());

//#### Authetnication endpoints

server.get('/auth/google',
    passport.authenticate('google', { scope:
        [ 'profile', 'email' ]
        })
    );

server.get('/auth/google/callback',
    passport.authenticate('google', {successRedirect: '/pass',
                                     failureRedirect: '/fail'})
    );

server.get('/logout', function (req, res) {
    req.logOut();
    res.redirect('/');
    });


const checkAuthenticated = (req, res, next) => {
    console.log('checkAuthenticated: entered')
    console.log(req._passport)
    if (req.isAuthenticated()) {
        console.log('authenticated')
        return next();
    }
    console.log('not authenticated')
    res.redirect('/fail', next);
};



// ################################## User Pages ####################################
server.get('/pass', checkAuthenticated, restify.serveStatic({
    directory: './public/',
    file: 'pass.html'
}));
server.get('/fail', restify.serveStatic({
    directory: './public/',
    file: 'fail.html'
}));

// ##################### REST endpoints #################################

//######################### Run server ##############################
server.on('uncaughtException', (req, res, route, err) => {
    console.log('uncaughtException');
    console.log(err);
});

server.listen(8080, () => console.log(`${server.name} listening at ${server.url}`));

// A utility function to safely escape JSON for embedding in a <script> tag
function safeStringify(obj) {
  return JSON.stringify(obj).replace(/<\/script/g, '<\\/script').replace(/<!--/g, '<\\!--')
}
