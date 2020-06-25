import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import SubscriberAPI from '../../SubscriberRole/SubscriberAPI'


it('renders without crashing', () => {
    shallow(<SubscriberAPI />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<SubscriberAPI />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#jumbotron').exists()).toBeDefined();
      expect(wrapper.find('#logout').exists()).toBeDefined();

      expect(wrapper.find('#display-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#open-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#personal-history-btn').exists()).toBeDefined();
      
  })
});