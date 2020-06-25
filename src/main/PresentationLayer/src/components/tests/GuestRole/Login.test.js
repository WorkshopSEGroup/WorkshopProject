import React from 'react';
import { shallow, mount, render } from '../../../enzyme';

import Login from '../../GuestRole/Login'



it('renders without crashing', () => {
    shallow(<Login />);
  });

describe('Login Test Suite', () => {

    // checking if the form elements exist.
    it('should render the form', () => {
        const wrapper = shallow(<Login />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.

        expect(wrapper.find('form.login').exists()).toBeDefined(); // check that the component renders ok
        expect(wrapper.find('#email').length).toEqual(1);   // id syntax - searched for email id
        expect(wrapper.find('#password').length).toEqual(1);    // id syntax - searched for password id
    })
});

describe('Email Test Suite', () => {

    it('should change the state of the Login component', () => {

        const wrapper = shallow(<Login />);
        // simulate an onChange event (when we enter an email input)
        wrapper.find('#email').simulate('change',
            {
                target: { name: 'nickname', value: 'web_app@mail.com' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.state('nickname')).toEqual('web_app@mail.com');  // check that state was changed
    })
})

describe('Password Test Suite', () => {

    it('should change the state of the Login component', () => {

        const wrapper = shallow(<Login />);
        wrapper.find('#password').simulate('change',
            {
                target: { name: 'password', value: 'password' }
            });
        wrapper.update();
        expect(wrapper.state('password')).toEqual('password');
    })
});