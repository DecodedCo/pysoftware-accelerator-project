
## PvWatts clone
* "A clone"
    * a private demo reporduction of a popular app/website
    * youtube: uber clones, netflix clones, amazon clones
* Front End
    * User-facing interface
    * Defines the requirements of most (business) software
        * this generates the technical reqs
    * Build wireframes
        * either, whiteboard sketches
        * maybe, generate with chatgpt

    
### Using ChatGPT to Generate wireframes (for clones)
* prompt for the technical specs of an app/interface
* prompt for a pure html/css wireframe
* iterate on these until the wireframe matches our target
    * eg., add in a results tab
* stop at some point, and fix the remaining issues man'ly

`
before the download card, add another called "results" which gives the pvwatts results screen including a placeholder for a graph 
`

### Manual, or try ChatGPT, for theme/css
* Add in, eg., bootstrap, and use bootstrap components to make the interface usaunle
* https://getbootstrap.com/docs/5.0/components/accordion/

`given the wireframe below for a pvwatts clone app, add in bootstrap css framework, and make the sections accordians`


### Sketching/Faking the API

* add in the wireframe to a new prompt
    * must have: the section for which data will be generated


`the below is a wireframe for a pvwatts clone app, with a results section. write a fake json response from a pvwatts api, and display it in the results section. `

` revise fakePVWattsResponse above, include all the relevant output variables from a real pvwatts model 
`

`provide the new results section with the relevant html parts as above`