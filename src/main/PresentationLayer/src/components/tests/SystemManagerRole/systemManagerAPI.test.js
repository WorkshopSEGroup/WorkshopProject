import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import systemManagerAPI from '../../SystemManagerRole/systemManagerAPI'


it('renders without crashing', () => {
    shallow(<systemManagerAPI />);
  });


describe('systemManagerAPI Test Suite', () => {

  // checking if the form elements exist and renders all elements
  it('should render the form', () => {
      const wrapper = shallow(<systemManagerAPI />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#jumbotron').exists()).toBeDefined();
      expect(wrapper.find('#logout').exists()).toBeDefined();

      expect(wrapper.find('#display-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#open-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#personal-history-btn').exists()).toBeDefined();
      expect(wrapper.find('#purchase-history-btn').exists()).toBeDefined();
      expect(wrapper.find('#visitors-cut-btn').exists()).toBeDefined();
      
  })
});

