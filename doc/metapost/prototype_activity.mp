input metauml;

iClass.foreColor := (1,1,1);

beginfig(1);
  Begin.b;
  Activity.download("Download needed data");
  Branch.missing_args;
  Activity.parse("Prepare data for output");
  Activity.output("Append data to output stream");
  End.e;

  leftToRight(30)(b, download);
  topToBottom(20)(download, missing_args, parse, output, e);

  drawObjects(b, download, missing_args, parse, output, e);

  clink(transition)(b, download);
  clink(transition)(download, missing_args);
  clink(transition)(missing_args, parse);
  clink(transition)(parse, output);
  clink(transition)(output, e);
  link(transition)(pathStepX(missing_args.e, e.e, 90));

  item(iGuard)("Needed arguments not given")(obj.sw = missing_args.s + (6, 6));
  item(iGuard)("All needed arguments given")(obj.ne = missing_args.s + (0, -1));

endfig;

end
