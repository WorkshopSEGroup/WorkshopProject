import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import RemoveManager from '../../OwnerOrManagerRole/RemoveManager'


it('renders without crashing', () => {
    shallow(<RemoveManager />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<RemoveManager />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#form').exists()).toBeDefined();
      expect(wrapper.find('#form-group').exists()).toBeDefined();
      expect(wrapper.find('#form-label').exists()).toBeDefined();
      expect(wrapper.find('#commit-btn').exists()).toBeDefined();
      
  })
});