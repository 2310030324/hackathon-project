import { Form } from "react-router-dom"

import {UserPlusIcon} from "@heroicons/react/24/solid"

import illustration from "../assets/illustration.jpg"
const Intro = () => {
  return (
    <div>
        <div>
      <h1>Take Control of <span className="accent">Your Money</span></h1>
      <p>personal budgeting is the secret to financial freedom. Start your journey today.</p>
        <Form method="post">
            <input type="text" 
            name="userName" 
            aria-label="Your Name" 
            autoComplete="given-name"/>
            <button type="submit">className="btn btn--dark</button>
            <span>Create Account</span>
            <UserPlusIcon width={20}/>
        </Form>
        </div>
    <img src={illustration} alt="person with money" width={60}/>
    </div>
  );
}
export default Intro