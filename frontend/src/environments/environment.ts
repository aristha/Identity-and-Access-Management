/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-dh8lpj82.us', // the auth0 domain prefix
    audience: 'http://localhost:5000/', // the audience set for the auth0 app
    clientId: '4zkei0fPLWHwPmIxwNrazq0pZAACIne8', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
