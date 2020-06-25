import React from 'react';
import { shallow, mount, render } from '../../../enzyme';

import RegisterForm from '../../GuestRole/RegisterForm'



it('renders without crashing', () => {
    shallow(<RegisterForm />);
  });

describe('RegisterForm Test Suite', () => {

    // checking if the form elements exist.
    it('should render the form', () => {
        const wrapper = shallow(<RegisterForm />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.

        expect(wrapper.find('form.register').exists()).toBeDefined(); // check that the component renders ok
        expect(wrapper.find('#email').length).toEqual(1);
        expect(wrapper.find('#password').length).toEqual(1);
    })
});

describe('Email Test Suite', () => {

    it('should change the state of the Register component', () => {

        const wrapper = shallow(<RegisterForm />);
        wrapper.find('#email').simulate('change',
            {
                target: { name: 'nickname', value: 'web_app@mail.com' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.state('nickname')).toEqual('web_app@mail.com');  // check that state was changed
    })
})

describe('Password Test Suite', () => {

    it('should change the state of the Register component', () => {

        const wrapper = shallow(<RegisterForm />);
        wrapper.find('#password').simulate('change',
            {
                target: { name: 'password', value: 'password' }
            });
        wrapper.update();
        expect(wrapper.state('password')).toEqual('password');
    })
});