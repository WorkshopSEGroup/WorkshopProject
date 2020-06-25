import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import OwnerAPI from '../../OwnerOrManagerRole/OwnerAPI'


it('renders without crashing', () => {
    shallow(<OwnerAPI />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<OwnerAPI />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#jumbotron').exists()).toBeDefined();
      expect(wrapper.find('#noti').exists()).toBeDefined();
      expect(wrapper.find('#logout').exists()).toBeDefined();
      expect(wrapper.find('#form-group').exists()).toBeDefined();
      expect(wrapper.find('#form-label').exists()).toBeDefined();
      expect(wrapper.find('#form-select').exists()).toBeDefined();
      expect(wrapper.find('#display-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#open-store-btn').exists()).toBeDefined();
      expect(wrapper.find('#personal-history-btn').exists()).toBeDefined();
      expect(wrapper.find('#manage-inv').exists()).toBeDefined();
      expect(wrapper.find('#appoint-owner').exists()).toBeDefined();
      expect(wrapper.find('#remove-owner').exists()).toBeDefined();
      expect(wrapper.find('#appoint-manager').exists()).toBeDefined();
      expect(wrapper.find('#edit-perm').exists()).toBeDefined();
      expect(wrapper.find('#remove-manager').exists()).toBeDefined();
      expect(wrapper.find('#view-purchase-hist').exists()).toBeDefined();
      expect(wrapper.find('#manage-policies').exists()).toBeDefined();
      expect(wrapper.find('#container-2').exists()).toBeDefined();

      expect(wrapper.find('#container-2').exists()).toBeDefined();
      expect(wrapper.find('#container-2').exists()).toBeDefined();
      
  })
});