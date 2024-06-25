---
layout: home 
permalink: /
title: "Home"
excerpt: "Social Feed Manager is open source software that harvests social media data and related content from Twitter, Tumblr, Flickr, and Sina Weibo."
image:
  feature: blue-bg.png
---
<div class="tiles">
  <div class="tile"><p>Social Feed Manager is open source software that harvests social media data and web resources from Twitter, Tumblr, Flickr, and Sina Weibo. 
  It empowers researchers, faculty, students, and archivists to collect, manage, and export social media data. By running Social Feed Manager on behalf of their communities, 
  cultural heritage and research organizations can provide an innovative service. </p>
  <p></p><strong>2024 Update</strong>: Because of changes to the Twitter/X API access model, we are no longer actively developing Social Feed Manager, nor are we providing a hosted instance at this time.</p> 
    <p>The Social Feed Manager software has been updated to work with the Twitter/X API v.2, and institutions or individuals wishing to deploy their own instances are welcome to do so. Members of the GW community doing social media research can consult with <a href="https://library.gwu.edu/collecting-social-media-data">GW Libraries staff</a> to learn about other tools to aid their research.</p>
  <p>For more information on Social Feed Manager, see <a href="{{ site.github.url }}/about/overview">Overview of Social Feed Manager</a> and the <a href="https://sfm.readthedocs.org">documentation</a>.</p> 
  </div>
  
  <div class="tile"><h2>Featured Posts</h2></div>
      {% for post in site.categories.top %}
    	  {% include post-grid.html %}
      {% endfor %}
  <div class="tile"><p><a href="{{ site.github.url }}/blog">See all posts</a></p></div> 
  <div class="tile"><p><img src="{{ site.github.url }}/images/nhprc-logo.png" width="100" alt="NHPRC logo" align="left" style="border:0">Social Feed Manager has been supported by a grant from the
  <a href="http://www.archives.gov/nhprc/">National Historical Publications & Records Commission</a> as well as grants from IMLS and the Council on East Asian Libraries.</p>
  </div>
</div><!-- /.tiles -->
