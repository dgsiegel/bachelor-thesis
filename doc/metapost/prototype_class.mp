input metauml;

iClass.foreColor := (1,1,1);

beginfig(1);
  Class.prototype("Prototype")()("+init_plugin_system()", "+find_plugins()");
  Class.plugin("Plugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.twitterapi("TwitterAPI")("-filecache")("+__init__(user, password, domain)");
  Class.twitterapicall("TwitterAPICall")("-user", "-password", "domain", "-uri", "-format", "-cache")("+__init__(cache, user, password, domain, uri)", "+__getattr__(arg)", "+__call__(args)");
  Class.filecache("FileCache")("-timeout", "-cache_dir")("+__init__()", "+is_cached(key)", "+get(key)", "+set(key, data)", "-_get_key_path(key)", "-_get_cache_time(key)");
  Class.twitterapierror("TwitterAPIError")()();

  Class.friendsplugin("FriendsPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.interestsplugin("InterestsPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.mailplugin("MailPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.locationplugin("LocationPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.repliesplugin("RepliesPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.sourcesplugin("SourcesPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.textsearchplugin("TextsearchPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.timesplugin("TimesPlugin")()("+download(api, args)", "+parse()", "+output(page)");
  Class.userplugin("UserPlugin")()("+download(api, args)", "+parse()", "+output(page)");


  plugin.n = prototype.ne + (350, 0);

  centered_allign_top(twitterapi, twitterapicall)(30, below(prototype.s, 100));
  centered_allign_top(filecache, twitterapierror)(30, below(prototype.s, 230));

  centered_allign_top(friendsplugin, interestsplugin)(10, below(plugin.s, 20));
  centered_allign_top(mailplugin, locationplugin)(10, below(plugin.s, 80));
  centered_allign_top(repliesplugin, sourcesplugin)(10, below(plugin.s, 140));
  centered_allign_top(textsearchplugin, timesplugin)(10, below(plugin.s, 200));
  userplugin.n = textsearchplugin.s + (0, -6);

  drawObjects(prototype, plugin, twitterapi, twitterapicall, twitterapierror, filecache);
  drawObjects(friendsplugin, interestsplugin, mailplugin, locationplugin, repliesplugin, sourcesplugin, textsearchplugin, timesplugin, userplugin);

  link(aggregation)(pathStepY(prototype.e, plugin.n, 50));

  link(aggregation)(pathStepX(prototype.w, twitterapi.n, -43));
  link(aggregation)(pathStepY(twitterapi.s, filecache.n, 0));
  link(aggregation)(pathStepX(twitterapi.e, twitterapicall.w, 0));
  link(aggregation)(pathStepX(twitterapi.e, twitterapierror.w, 10));

  link(inheritance)(pathStepX(plugin.w, friendsplugin.w, -75));
  link(inheritance)(pathStepX(plugin.w, mailplugin.w, -75));
  link(inheritance)(pathStepX(plugin.w, repliesplugin.w, -75));
  link(inheritance)(pathStepX(plugin.w, textsearchplugin.w, -75));
  link(inheritance)(pathStepX(plugin.w, userplugin.w, -75));

  link(inheritance)(pathStepX(plugin.e, interestsplugin.e, 75));
  link(inheritance)(pathStepX(plugin.e, locationplugin.e, 75));
  link(inheritance)(pathStepX(plugin.e, sourcesplugin.e, 75));
  link(inheritance)(pathStepX(plugin.e, timesplugin.e, 75));
endfig;

end
